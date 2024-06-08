from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from config.config import Config


class AlipayConfig:
    """
    支付宝配置类，初始化时生成客户端对象以便复用
    """

    def __init__(self):
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = Config.GATEWAY_URL
        alipay_client_config.app_id = Config.APP_ID
        alipay_client_config.app_private_key = Config.APP_PRIVATE_KEY
        alipay_client_config.alipay_public_key = Config.ALIPAY_PUBLIC_KEY
        alipay_client_config.charset = Config.CHARSET
        alipay_client_config.format = Config.FORMAT
        alipay_client_config.sign_type = Config.SIGN_TYPE
        self.client = DefaultAlipayClient(alipay_client_config)


alipay_config = AlipayConfig()
