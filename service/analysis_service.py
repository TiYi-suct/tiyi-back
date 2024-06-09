"""
音频分析服务
"""
import inspect
import io
import logging
import uuid
from functools import wraps

import librosa
import numpy as np
from flask import g
from matplotlib import pyplot as plt

from config.config import Config
from model.models import Audio, User, AnalysisItem, db
from utils.response import Response

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

            # todo 优先从本地获取结果

            try:
                # 进行音频分析
                result = f(*args, **kwargs)
                # todo 返回结果之前先缓存记录
                return result
            except Exception as e:
                logging.error(f'{analysis_item_name} 分析出现异常：{audio_id}, 错误信息：{e}')
                # 返还用户音乐币
                if not return_music_coin(username, analysis_item_name):
                    return Response.error(f'{analysis_item_name}：音乐币返还异常，请联系工作人员')
                return Response.error(f'{analysis_item_name} 分析出现异常')

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
    except:
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
    except:
        logging.error(f'返还音乐币出现异常，用户：{username}，数量：{analysis_item.price}')
        db.session.rollback()
        return False


# 截取音频片段，以秒为单位
def get_audio_segment(audio_id, start_time, end_time):
    audio = Audio.query.filter_by(audio_id=audio_id).first()
    if not audio:
        raise AudioNotFoundError('音频记录不存在')
    # 加载音频文件，
    y, sr = librosa.load(audio.local_path, sr=None)
    # 打印采样率和音频数据长度以进行调试
    print(f"Sample rate: {sr}")
    print(f"Audio length: {len(y)} samples")

    # 转换起始时间和结束时间为样本索引
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr) if end_time > 0 else len(y)

    # 检查起始时间范围
    if start_sample > len(y) or start_sample > end_sample:
        raise InvalidBoundError(
            f'范围参数错误，开始时间：{start_time}，结束时间：{end_time}，开始索引：{start_sample}，结束索引：{end_sample}，实际范围：{len(y)}')

    # 确保索引不超出范围
    start_sample = max(0, start_sample)
    end_sample = min(len(y), end_sample)

    # 截取指定的音频片段
    y = y[start_sample:end_sample]
    return y, sr


class AudioNotFoundError(Exception):
    pass


class InvalidBoundError(Exception):
    pass


@analysis_process('梅尔频谱图')
def mel_spectrogram(audio_id, start_time, end_time):
    y, sr = get_audio_segment(audio_id, start_time, end_time)
    # 计算梅尔频谱图
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    mel_spectrogram_db = librosa.power_to_db(mel, ref=np.max)
    # 创建绘图
    fig, ax = plt.subplots(figsize=(10, 4))
    img = librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel', ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel Spectrogram')
    # 保存图像到内存文件
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    filename = uuid.uuid4().hex + '.png'
    # 将图像保存到本地
    image_path = f'{Config.STORE_FOLDER}/{filename}'
    with open(image_path, 'wb') as f:
        f.write(buf.getbuffer())
    url = f'{Config.SERVER_URL}/file/{filename}'
    return Response.success(url)
