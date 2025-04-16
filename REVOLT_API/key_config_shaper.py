import base64
from typing import Union, Optional
from uuid import UUID
from dao.select_methods_dao import get_user_info
from XUI.methods import get_connection_string
import logging

logger = logging.getLogger(__name__)


async def generate_config_key(user_id: Union[str, UUID]) -> Optional[str]:
    try:
        user = await get_user_info(user_id=user_id)
        if user is None or user.is_active == False:
            return 'Subscription not detected'

        server = user.connections.server

        panel_url = server.panel_url
        address = server.address
        port = server.port
        tag = user.connections.tag

        vless_key = await get_connection_string(user_id=user_id,
                                                server_address=address,
                                                server_port=port,
                                                tag=tag,
                                                panel_url=panel_url)

        b = base64.b64encode(bytes(vless_key, 'utf-8'))
        base64_vless_key = b.decode('utf-8')

        return base64_vless_key

    except Exception as e:
        logger.error(e)
        return None