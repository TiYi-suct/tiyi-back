import uuid

import librosa
import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from config.config import Config

# 使用Agg后端，在无GUI的服务器上使用
matplotlib.use('Agg')


# 梅尔频谱图
def mel_spectrogram_task(path, start_time, end_time):
    y, sr = get_audio_segment(path, start_time, end_time)
    # 计算梅尔频谱图
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)  # type: ignore
    # 转换为分贝
    S_db = librosa.power_to_db(mel, ref=np.max)
    # 绘制梅尔频谱图
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()
    # 将图像保存到本地
    return save_analysis_img()


# 频谱图
def spectrogram_task(path, start_time, end_time):
    y, sr = get_audio_segment(path, start_time, end_time)
    # 计算短时傅里叶变换（STFT）
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    # 绘制频谱图
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_db, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    return save_analysis_img()


# BPM
def bpm_task(path, start_time, end_time):
    y, sr = get_audio_segment(path, start_time, end_time)
    # 监测节拍
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    # BPM只有一个数
    return tempo.item()


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
def save_analysis_img():
    filename = uuid.uuid4().hex + '.png'
    image_path = f'{Config.STORE_FOLDER}/{filename}'
    plt.savefig(image_path, format='png')
    plt.close()
    url = f'{Config.SERVER_URL}/file/{filename}'
    return url


# 截取范围异常
class InvalidBoundError(Exception):
    pass
