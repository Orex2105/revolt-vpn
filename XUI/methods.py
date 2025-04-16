from py3xui import AsyncApi
from XUI.panel_api import login
from random import randint
from typing import Optional
from config import XUISettings
import logging

logger = logging.getLogger(__name__)


@login
async def get_connection_string(user_id: str,
                                panel_url: str,
                                server_address: str,
                                server_port: int,
                                inbound_id: int=1,
                                tag: Optional[str]=None,
                                xui_api: Optional[AsyncApi] = None) -> Optional[str]:

    """
    :param user_id: uuid клиента
    :param panel_url: url x-ui панели. Используется декоратором для авторизации
    :param server_address: ip сервера
    :param server_port: порт на сервере для подключения
    :param inbound_id: id блока соединений
    :param tag: тэг для идентификации ключа
    :param xui_api: экземпляр класса AsyncApi. Передается декоратором
    :return: строка подключения или None
    """
    try:
        inbound = await xui_api.inbound.get_by_id(inbound_id)

        public_key = inbound.stream_settings.reality_settings["settings"]["publicKey"]
        website_name = inbound.stream_settings.reality_settings["serverNames"][0]
        short_id = inbound.stream_settings.reality_settings["shortIds"][0]
        flow = inbound.stream_settings.reality_settings.get("flow", "xtls-rprx-vision")

        emojis = XUISettings.EMOJIS
        random_emoji = emojis[randint(0, len(emojis) - 1)]

        connection_string = (
            f"vless://{user_id}@{server_address}:{server_port}"
            f"?type=tcp&security=reality&pbk={public_key}&fp=chrome&sni={website_name}"
            f"&sid={short_id}&spx=%2F&flow={flow}#{tag if tag else ''}{random_emoji}"
        )
        return connection_string

    except Exception as e:
        logger.error(e)
        return None