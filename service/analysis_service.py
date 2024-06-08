"""
音频分析服务
"""
import io
import logging
import sys
import uuid

import librosa
import numpy as np
from matplotlib import pyplot as plt

from config.config import Config
from model.models import Audio, User, AnalysisItem, db
from utils.response import Response


class AnalysisService:
    @staticmethod
    def mel_spectrogram(username, audio_id, start_time, end_time):
        # 首先扣减音乐币
        analysis_item_name = '梅尔频谱图'
        is_deducted = deduct_music_coin(username, analysis_item_name)
        if not is_deducted:
            return Response.error('音乐币不足')
        # todo 优先从本地获取结果
        try:
            y, sr = get_audio_segment(audio_id, start_time, end_time)
            # 计算梅尔频谱图
            mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
            mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
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
            # todo 将分析记录缓存到本地
            url = f'{Config.SERVER_URL}/file/{filename}'
            return Response.success(url)
        except Exception:
            # 扣减后分析失败返还音乐币
            if is_deducted:
                if not return_music_coin(username, analysis_item_name):
                    return Response.error(f'{analysis_item_name}：音乐币返还异常，请联系工作人员')
            logging.error(f'获取梅尔频谱图出现异常：{audio_id}')
            return Response.error('获取梅尔频谱图出现异常')


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

    # 确保索引不超出范围
    start_sample = max(0, start_sample)
    end_sample = min(len(y), end_sample)

    # 添加调试信息
    print(f"Start sample: {start_sample}")
    print(f"End sample: {end_sample}")

    # 截取指定的音频片段
    y = y[start_sample:end_sample]
    return y, sr


class AudioNotFoundError(Exception):
    pass
