'''import base64
from typing import Union
from uuid import UUID
from dao.select_methods_dao import get_user_info


async def generate_config_key(user_id: Union[str, UUID]) -> str:
    user = await get_user_info(user_id=user_id)
    if user is None or user.is_active == False:
        return 'Subscription not detected'

    server = user.connections.server
    panel_url = server.panel_url
    server_address = server.address'''
# НУЖНО ДОПИСАТЬ