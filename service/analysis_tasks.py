import logging
import uuid

import librosa
import matplotlib
import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt

from config.config import Config

"""
分析任务需要提交到单独的进程中进行，提交到进程池的任务不能被装饰器修饰，因此单独分离此模块
"""

# 使用Agg后端，在无GUI的服务器上使用
matplotlib.use('Agg')


# 梅尔频谱图
def mel_spectrogram_task(path, start_time, end_time):
    try:
        y, sr = get_audio_segment(path, start_time, end_time)
        # 计算梅尔频谱图
        mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)  # type: ignore
        # 转换为分贝
        S_db = librosa.power_to_db(mel, ref=np.max)
        # 绘制梅尔频谱图
        plt.figure(figsize=(calc_fig_width(y, sr), 6))
        librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel Spectrogram')
        plt.tight_layout()
        # 将图像保存到本地
        return save_analysis_img()
    except Exception as e:
        logging.error('梅尔频谱图：', e)
        raise e
    finally:
        plt.close()


# 频谱图
def spectrogram_task(path, start_time, end_time):
    try:
        y, sr = get_audio_segment(path, start_time, end_time)
        # 计算短时傅里叶变换（STFT）
        D = librosa.stft(y)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        # 绘制频谱图
        plt.figure(figsize=(calc_fig_width(y, sr), 6))
        librosa.display.specshow(S_db, x_axis='time', y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Spectrogram')
        plt.tight_layout()
        return save_analysis_img()
    except Exception as e:
        logging.error('频谱图：', e)
        raise e
    finally:
        plt.close()


# BPM
def bpm_task(path, start_time, end_time):
    try:
        y, sr = get_audio_segment(path, start_time, end_time)
        # 监测节拍
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        # BPM只有一个数
        return tempo.item()
    except Exception as e:
        logging.error('BPM：', e)
        raise e


# 移调
def transposition_task(path, start_time, end_time, n_steps):
    try:
        y, sr = get_audio_segment(path, start_time, end_time)
        # 移调后的音频
        y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=n_steps)
        # 将音频保存到本地，返回url
        return save_analysis_audio(y_shifted, sr, get_ext(path))
    except Exception as e:
        logging.error('移调：', e)
        raise e


# MFCC
def mfcc_task(path, start_time, end_time, n_mfcc=20):
    try:
        y, sr = get_audio_segment(path, start_time, end_time)
        # 计算MFCC
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)  # type: ignore
        # 绘图
        plt.figure(figsize=(calc_fig_width(y, sr), 2 * n_mfcc))
        for i in range(n_mfcc):
            plt.subplot(n_mfcc, 1, i + 1)
            plt.plot(mfccs[i])
            plt.title(f'MFCC Coefficient {i + 1}')
            plt.xlabel('Time Frame')
            plt.ylabel('Amplitude')
        plt.tight_layout()
        return save_analysis_img()
    except Exception as e:
        logging.error('MFCC：', e)
        raise e
    finally:
        plt.close()


# 截取音频片段，以秒为单位
def get_audio_segment(path, start_time, end_time):
    # 加载音频文件，
    y, sr = librosa.load(path, sr=None)

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


# 保存图片，返回远程访问地址
def save_analysis_img(ext='png'):
    filename = uuid.uuid4().hex + '.' + ext
    image_path = f'{Config.STORE_FOLDER}/{filename}'
    plt.savefig(image_path, format=ext)
    plt.close()
    url = f'{Config.SERVER_URL}/file/{filename}'
    return url


# 获取文件格式
def get_ext(path):
    return path.split('.')[-1]


# 保存音频，返回远程访问地址
def save_analysis_audio(y, sr, ext):
    filename = uuid.uuid4().hex + '.' + ext
    audio_path = f'{Config.STORE_FOLDER}/{filename}'
    sf.write(audio_path, y, sr, format=ext)
    url = f'{Config.SERVER_URL}/file/{filename}'
    return url


# 每秒对应的图形宽度
width_per_second = 0.3


# 计算图片的宽度：与音频的长度有关
def calc_fig_width(y, sr):
    duration = librosa.get_duration(y=y, sr=sr)
    width = duration * width_per_second
    return width if width > 10 else 10


# 截取范围异常
class InvalidBoundError(Exception):
    pass
