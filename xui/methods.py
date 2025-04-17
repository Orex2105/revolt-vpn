from py3xui import AsyncApi, Client
from xui.panel_api import login
from random import randint
from typing import Optional, Union
from config import XUISettings
from uuid import UUID
from time import time
import datetime
import logging
from pydantic_models.models import ServerStatus

logger = logging.getLogger(__name__)


@login
async def add_new_client(user_tg_id: Union[str, int],
                         user_id: Union[str, UUID],
                         panel_url: str,
                         subscription_duration: int,
                         inbound_id: int=1,
                         flow: str='xtls-rprx-vision',
                         limit_ip: int=1,
                         xui_api: Optional[AsyncApi]=None
                         ) -> None:
    """
    :param user_tg_id: tg id пользователя
    :param user_id: uuid пользователя
    :param panel_url: url x-ui панели. Используется декоратором для авторизации
    :param subscription_duration: длительность подписки (в днях). 0 - без ограничения
    :param inbound_id: id блока соединений
    :param flow: способ управления трафиком
    :param limit_ip: лимит ip
    :param xui_api: экземпляр класса AsyncApi. Передается декоратором
    :return: None
    """
    try:
        if subscription_duration != 0:
            expiry_time = int(time() * 1000) + subscription_duration * 86400 * 1000
        else:
            expiry_time = 0

        new_client = Client(
            id=user_id,
            email=str(user_tg_id),
            flow=flow,
            limit_ip=limit_ip,
            enable=True,
            expiry_time=expiry_time)

        await xui_api.client.add(inbound_id, [new_client])
    except Exception as e:
        logger.error(e)


@login
async def get_connection_string(user_id: Union[str, UUID],
                                panel_url: str,
                                server_address: str,
                                server_port: int,
                                inbound_id: int=1,
                                tag: Optional[str]=None,
                                xui_api: Optional[AsyncApi]=None) -> Optional[str]:
    """
    :param user_id: uuid пользователя
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
            f"&sid={short_id}&spx=%2F&flow={flow}#{tag if tag else ''} {random_emoji}"
        )
        return connection_string

    except Exception as e:
        logger.error(e)
        return None


@login
async def get_server_status(panel_url: str,
                            xui_api: Optional[AsyncApi]=None):

    server_status = await xui_api.server.get_status()

    return ServerStatus(
        cpu_load=round(server_status.cpu, 2),
        cpu_cores=server_status.cpu_cores,
        cpu_speed=round(server_status.cpu_speed_mhz / 1000, 2),
        memory_usage=round(server_status.mem.current / 1024 ** 3, 2),
        memory_total=round(server_status.mem.total / 1024 ** 3, 2),
        disk_memory_total=round(server_status.disk.total / (1024**3), 2),
        disk_memory_current=round(server_status.disk.current / (1024**3), 2),
        public_ip_v4=server_status.public_ip.ipv4,
        public_ip_v6=server_status.public_ip.ipv6,
        uptime=server_status.uptime,
        xray_state=server_status.xray.state,
        xray_version=server_status.xray.version,
    )