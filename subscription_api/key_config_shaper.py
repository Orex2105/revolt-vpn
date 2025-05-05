from typing import Union, Optional
from uuid import UUID
from pydantic_models.models import ClientTraffic
from utils.cache import DataCache
from xui.methods import XuiAPI
import logging

logger = logging.getLogger(__name__)


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


async def get_traffic(user_id: Union[str, UUID]):
    connection = await DataCache.connection(user_id=user_id)
    panel_url = connection.server.panel_url
    traffic = await XuiAPI.get_subscription_userinfo(user_id=user_id,panel_url=panel_url)

    return ClientTraffic(
        up = traffic[0].up if traffic else 0,
        down = traffic[0].down if traffic else 0,
        total = (traffic[0].up if traffic else 0) + (traffic[0].down if traffic else 0)
    )