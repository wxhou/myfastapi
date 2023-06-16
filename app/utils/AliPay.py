from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.util.SignatureUtils import verify_with_rsa
from app.settings import settings
from app.utils.logger import logger


class AliPay(object):

    def __init__(self) -> None:
        self.logger = logger.bind(alipay=True)
        self.server_url = settings.ALIPAY_SERVER_URL
        self.app_id = settings.ALIPAY_APP_ID
        self.app_private_key = settings.ALIPAY_APP_PRIVATE_KEY
        self.alipay_public_key = settings.ALIPAY_PUBLIC_KEY


    def config(self):
        alipay_client_config = AlipayClientConfig(sandbox_debug=True)
        alipay_client_config.server_url = self.server_url
        alipay_client_config.app_id = self.app_id
        alipay_client_config.app_private_key = self.app_private_key
        alipay_client_config.alipay_public_key = self.alipay_public_key
        return alipay_client_config

    def client(self) -> DefaultAlipayClient:
        _client = DefaultAlipayClient(alipay_client_config=self.config(),
                            logger=self.logger)
        return _client


ALIPAY = AliPay()