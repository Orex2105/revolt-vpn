import logging
from aiocache import cached, caches
from dao.select_methods_dao import get_all_admins, get_user_info, get_connection_info
from typing import Union, Optional
from uuid import UUID
from database_utils.models import Users

logger = logging.getLogger(__name__)


class DataCache:
    admins_cache_ttl = 600
    users_cache_ttl = 30

    @classmethod
    @cached(admins_cache_ttl)
    async def admins(cls) -> Optional[list[int]]:
        try:
            return await get_all_admins()
        except Exception as e:
            logger.error(e)


    @classmethod
    @cached(users_cache_ttl)
    async def user(cls, user_id: Union[str, UUID]) -> Optional[Users]:
        try:
            return await get_user_info(user_id=user_id)
        except Exception as e:
            logger.error(e)


    @classmethod
    @cached(users_cache_ttl)
    async def connection(cls, user_id: Union[str, UUID]) -> Optional[Users]:
        try:
            return await get_connection_info(user_id=user_id)
        except Exception as e:
            logger.error(e)


    @classmethod
    async def startup_cache(cls):
        await cls.admins()


    @classmethod
    async def cache_cleaner(cls) -> None:
        await caches.get("default").clear()