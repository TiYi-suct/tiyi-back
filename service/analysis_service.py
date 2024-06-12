"""
音频分析服务
"""
import inspect
import json
import logging
import threading
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from functools import wraps

from flask import g

from config.redis_config import redis_client
from model.models import User, AnalysisItem, db, Audio
from service.analysis_tasks import mel_spectrogram_task, spectrogram_task, bpm_task, transposition_task, mfcc_task
from utils.response import Response

"""
自定义进程池
"""


class ResilientProcessPoolExecutor(ProcessPoolExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._broken = False

    def submit(self, fn, *args, **kwargs):
        if self._broken:
            raise BrokenProcessPool("Process pool is broken")
        try:
            return super().submit(fn, *args, **kwargs)
        except BrokenProcessPool:
            self._broken = True
            raise

    def is_broken(self):
        return self._broken


lock = threading.Lock()

# 全局进程池，处理绘图多线程安全问题
executor = ResilientProcessPoolExecutor()


# 根据函数签名计算key
def cache_key(f, *args, **kwargs):
    return f.__name__ + str(args) + str(kwargs)


def restart_pool():
    global executor
    with lock:
        # 判断进程池是否不可用
        if executor is None or executor.is_broken():
            executor = ResilientProcessPoolExecutor(max_workers=4)


"""
音频分析流程装饰器：
1. 首先扣减用户音乐币
2. 分析音频
3. 如果分析过程出现异常，返还音乐币
"""


def analysis_process(analysis_item_name):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # 检查必要的参数
            func_args = inspect.signature(f).bind(*args, **kwargs).arguments
            audio_id = func_args.get('audio_id')
            start_time = func_args.get('start_time')
            end_time = func_args.get('end_time')
            if audio_id is None or start_time is None or end_time is None:
                return Response.error('缺少必要的参数')

            # 从全局对象获取 username
            username = g.get('username')
            if not username:
                return Response.error('用户未登录')

            # 扣减音乐币
            is_deducted = deduct_music_coin(username, analysis_item_name)
            if not is_deducted:
                return Response.error('音乐币不足')

            # 优先从本地获取结果
            key = cache_key(f, *args, **kwargs)
            cache_result = redis_client.get(key)
            if cache_result:
                cache_result = json.loads(cache_result)
                logging.info(f'命中缓存：key:{key},value:{cache_result}')
                return cache_result, 200

            try:
                # 在单独的进程中进行音频分析
                result, code = f(*args, **kwargs)
                # 返回结果之前先缓存记录
                logging.info(f'缓存到redis：key：{key},value:{result}')
                redis_client.set(key, json.dumps(result))
                return result, code
            except BrokenProcessPool:
                logging.warning("Process pool is broken. Reinitializing.")
                restart_pool()  # Reinitialize the global executor
                raise Exception('分析进程池异常，已重启，请稍后重试')
            except Exception as e:
                logging.error(f'{analysis_item_name}分析出现异常：{audio_id}, 错误信息：{e}')
                # 返还用户音乐币
                if not return_music_coin(username, analysis_item_name):
                    return Response.error(f'{analysis_item_name}：音乐币返还异常，请联系工作人员')
                return Response.error(f'{analysis_item_name}分析出现异常：{e}')

        return decorated

    return decorator


# 扣减用户音乐币
def deduct_music_coin(username, analysis_item_name):
    user = User.query.filter_by(username=username).first()
    analysis_item = AnalysisItem.query.filter_by(name=analysis_item_name).first()
    if not user or not analysis_item:
        return False
    if user.music_coin < analysis_item.price:
        return False
    try:
        user.music_coin -= analysis_item.price
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f'扣减用户音乐币异常，用户名：{username}，分析项：{analysis_item_name}，错误信息：{e}')
        db.session.rollback()
        return False


# 返还用户音乐币
def return_music_coin(username, analysis_item_name):
    user = User.query.filter_by(username=username).first()
    analysis_item = AnalysisItem.query.filter_by(name=analysis_item_name).first()
    if not user or not analysis_item:
        return False
    try:
        user.music_coin += analysis_item.price
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f'返还音乐币出现异常，用户：{username}，数量：{analysis_item.price}，错误信息：{e}')
        db.session.rollback()
        return False


# 获取音频文件路径
def get_audio_path(audio_id):
    audio = Audio.query.filter_by(audio_id=audio_id).first()
    if not audio:
        raise AudioNotFoundError('音频记录不存在')
    return audio.local_path


@analysis_process('梅尔频谱图')
def mel_spectrogram(audio_id, start_time, end_time):
    path = get_audio_path(audio_id)
    return Response.success(executor.submit(mel_spectrogram_task, path, start_time, end_time).result())


@analysis_process('频谱图')
def spectrogram(audio_id, start_time, end_time):
    path = get_audio_path(audio_id)
    future = executor.submit(spectrogram_task, path, start_time, end_time)
    return Response.success(future.result())


@analysis_process('BPM')
def bpm(audio_id, start_time, end_time):
    path = get_audio_path(audio_id)
    return Response.success(executor.submit(bpm_task, path, start_time, end_time).result())


@analysis_process('移调')
def transposition(audio_id, start_time, end_time, n_steps):
    path = get_audio_path(audio_id)
    return Response.success(executor.submit(transposition_task, path, start_time, end_time, n_steps).result())


@analysis_process('MFCC')
def mfcc(audio_id, start_time, end_time, n_mfcc=20):
    path = get_audio_path(audio_id)
    return Response.success(executor.submit(mfcc_task, path, start_time, end_time, n_mfcc).result())


# 音频不存在
class AudioNotFoundError(Exception):
    pass
