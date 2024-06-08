import os

"""
项目配置类
"""


class Config:
    # 数据库连接
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 文件保存目录
    AUDIO_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files', 'audios')
    SERVER_URL = os.getenv('SERVER_URL')
    # 支付宝支付
    GATEWAY_URL = os.getenv('GATEWAY_URL')
    APP_ID = os.getenv('APP_ID')
    APP_PRIVATE_KEY = os.getenv('APP_PRIVATE_KEY')
    ALIPAY_PUBLIC_KEY = os.getenv('ALIPAY_PUBLIC_KEY')
    CHARSET = os.getenv('CHARSET')
    FORMAT = os.getenv('FORMAT')
    SIGN_TYPE = os.getenv('SIGN_TYPE')
