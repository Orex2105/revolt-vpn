from typing import Optional
from pydantic_models.models import ClientSubData
from utils.cache import DataCache
from datetime import datetime
from xui.methods import XuiAPI
import base64
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='web.SubApiHelper')


class SubscriptionApiHelper:
    @staticmethod
    async def generate_config_key(telegram_id: str) -> Optional[list[str]]:
        config = []
        try:
            subscription = await DataCache.subscription(telegram_id=telegram_id)

            if subscription is None or (subscription.end_date < datetime.now()):
                return None

            servers = await DataCache.servers()

            for server in servers:
                panel_url = server.panel_url
                login = server.login
                password = server.password
                address = server.ip_address
                port = server.port
                tag = server.country.name
                inbound_id = server.inbound_id

                vless_key = await XuiAPI.get_connection_string(telegram_id=telegram_id,
                                                               server_address=address,
                                                               server_port=port,
                                                               tag=tag,
                                                               panel_url=panel_url,
                                                               login=login,
                                                               password=password,
                                                               inbound_id=inbound_id)
                if vless_key is not None:
                    config.append(vless_key)
            return config
        except Exception as e:
            logger.error(e)
            return None


    @staticmethod
    async def get_traffic(telegram_id: str) -> Optional[ClientSubData]:
        try:
            servers = await DataCache.servers()

            up = 0
            down = 0
            total_spent = 0
            limitation = 0
            expiry_time = 0

            for server in servers:
                panel_url = server.panel_url
                login = server.login
                password = server.password
                client_data = await XuiAPI.get_subscription_userinfo(user_id=telegram_id, panel_url=panel_url,
                                                                     password=password, login=login)

                up += client_data[0].up if client_data else 0
                down += client_data[0].down if client_data else 0
                total_spent += up + down
                limitation = client_data[0].total if client_data else 0
                expiry_time = client_data[0].expiry_time if client_data else 0

            return ClientSubData(
                up = up,
                down = down,
                total_spent = total_spent,
                limitation = limitation,
                expiry_time = expiry_time
            )
        except Exception as e:
            logger.error(e)
            return None


    @staticmethod
    def encode_title(text: str) -> str:
        b64 = base64.b64encode(text.encode('utf-8')).decode('ascii')
        return f"base64:{b64}"