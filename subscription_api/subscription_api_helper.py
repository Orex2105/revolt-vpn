from typing import Union, Optional
from uuid import UUID
from pydantic_models.models import ClientSubData
from utils.cache import DataCache
from xui.methods import XuiAPI
import base64
import logging

logger = logging.getLogger(__name__)


class SubscriptionApiHelper:
    @staticmethod
    async def generate_config_key(user_id: Union[str, UUID]) -> Optional[str]:
        try:
            user = await DataCache.user(user_id=user_id)

            if user is None or user.is_active == False:
                return None

            server = user.connections.server
            is_archived = user.connections.is_archived
            panel_url = server.panel_url
            address = server.address
            port = server.port
            tag = server.location

            if not is_archived:
                vless_key = await XuiAPI.get_connection_string(user_id=user_id,
                                                        server_address=address,
                                                        server_port=port,
                                                        tag=tag,
                                                        panel_url=panel_url)
                return vless_key
            else:
                return None

        except Exception as e:
            logger.error(e)
            return None


    @staticmethod
    async def get_traffic(user_id: Union[str, UUID]) -> ClientSubData:
        connection = await DataCache.connection(user_id=user_id)
        panel_url = connection.server.panel_url
        client_data = await XuiAPI.get_subscription_userinfo(user_id=user_id,panel_url=panel_url)

        return ClientSubData(
            up = client_data[0].up if client_data else 0,
            down = client_data[0].down if client_data else 0,
            total_spent = (client_data[0].up if client_data else 0) + (client_data[0].down if client_data else 0),
            limitation = client_data[0].total if client_data else 0,
            expiry_time = client_data[0].expiry_time if client_data else 0
        )


    @staticmethod
    def encode_title(text: str) -> str:
        b64 = base64.b64encode(text.encode('utf-8')).decode('ascii')
        return f"base64:{b64}"