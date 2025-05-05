import logging
from functools import lru_cache
from aiocache import cached, caches
from aiogram.types import BufferedInputFile
import qrcode
import io
from dao.select_methods_dao import get_all_admins, get_user_info, get_connection_info
from typing import Union, Optional
from uuid import UUID, uuid5, NAMESPACE_DNS
from database_utils.models import Users, Connections
from pydantic_models.models import ServerIsAlive
from utils.ping import is_alive
from xui.methods import XuiAPI

logger = logging.getLogger(__name__)


class DataCache:
    admins_cache_ttl = 600
    users_cache_ttl = 60
    connections_cache_ttl = 30
    server_status_cache_ttl = 300
    xui_online_list_cache_ttl = 10


    @staticmethod
    @lru_cache(maxsize=100)
    def uuid5_hashing(user_id: Union[str, UUID]) -> UUID:
        return uuid5(NAMESPACE_DNS, str(user_id))

    @staticmethod
    @lru_cache(maxsize=100)
    def qr(data: str) -> BufferedInputFile:
        _qr = qrcode.make(data, box_size=6)
        _buffer = io.BytesIO()
        _qr.save(_buffer, format='PNG')
        _buffer.seek(0)

        return BufferedInputFile(_buffer.read(), filename="qr.png")


    @classmethod
    @cached(admins_cache_ttl)
    async def admins(cls) -> Optional[list[int]]:
        try:
            return await get_all_admins()
        except Exception as e:
            logger.error(e)
            return None


    @classmethod
    @cached(users_cache_ttl)
    async def user(cls, user_id: Union[str, UUID]) -> Optional[Users]:
        try:
            return await get_user_info(user_id=user_id)
        except Exception as e:
            logger.error(e)


    @classmethod
    @cached(connections_cache_ttl)
    async def connection(cls, user_id: Union[str, UUID]) -> Optional[Connections]:
        try:
            return await get_connection_info(user_id=user_id)
        except Exception as e:
            logger.error(e)


    @classmethod
    @cached(server_status_cache_ttl)
    async def server_status(cls, host, port) -> ServerIsAlive:
        return await is_alive(host=host, port=port)


    @classmethod
    async def startup_cache(cls) -> bool:
        if await cls.admins():
            return True
        else:
            return False


    @staticmethod
    async def cache_cleaner() -> None:
        await caches.get("default").clear()


    @classmethod
    @cached(xui_online_list_cache_ttl)
    async def server_users_online(cls, panel_url) -> list[str]:
        try:
            return await XuiAPI.get_online_clients(panel_url=panel_url)
        except Exception as e:
            logger.error(e)
            return []