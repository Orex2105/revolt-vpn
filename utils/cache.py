from functools import lru_cache
from aiocache import cached, caches
from aiogram.types import BufferedInputFile
import qrcode
import io
from dao.select_methods_dao import all_admins, user_info, subscription_info, all_servers
from typing import Union, Optional
from database_utils.models import User, Subscription, Server
from pydantic_models.models import ServerIsAlive
from utils.ping import is_alive
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='utils.Cache')


class DataCache:
    admins_cache_ttl = 600
    users_cache_ttl = 60
    subscriptions_cache_ttl = 60
    server_status_cache_ttl = 300
    servers_list_cache_ttl = 300
    xui_online_list_cache_ttl = 10


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
            return await all_admins()
        except Exception as e:
            logger.error(e)
            return None


    @classmethod
    @cached(servers_list_cache_ttl)
    async def servers(cls) -> Optional[list[Server]]:
        try:
            return await all_servers()
        except Exception as e:
            logger.error(e)
            return None


    @classmethod
    @cached(users_cache_ttl)
    async def user(cls, telegram_id: Union[str, int]) -> Optional[User]:
        try:
            return await user_info(telegram_id=int(telegram_id))
        except Exception as e:
            logger.error(e)


    @classmethod
    @cached(subscriptions_cache_ttl)
    async def subscription(cls, telegram_id: Union[str, int]) -> Optional[Subscription]:
        try:
            return await subscription_info(telegram_id=int(telegram_id))
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