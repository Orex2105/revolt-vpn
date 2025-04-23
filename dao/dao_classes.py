from dao.base_dao import BaseDAO
from database_utils.models import Users, Admins, Servers, Connections
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import Union, Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_user_info(cls, session: AsyncSession,
                            user_id: Union[str, UUID]) -> Optional[Users]:
        try:
            query = select(cls.model).where(cls.model.user_id == user_id)
            result = await session.execute(query)

            return result.unique().scalar_one_or_none()

        except Exception as e:
            logger.error(e)
            return None


    @classmethod
    async def update_last_seen(cls, session: AsyncSession, user_id: Union[str, UUID]) -> bool:
        try:
            query = update(cls.model).where(cls.model.user_id == user_id).values(last_seen=func.now())
            await session.execute(query)
            await session.commit()

            return True

        except Exception as e:
            logger.error(e)
            return False


class AdminsDAO(BaseDAO):
    model = Admins

    @classmethod
    async def get_admin_info(cls, session: AsyncSession,
                            tg_id: int) -> Optional[Admins]:
        try:
            query = select(cls.model).where(cls.model.tg_id == tg_id)
            result = await session.execute(query)

            return result.unique().scalar_one_or_none()

        except Exception as e:
            logger.error(e)
            return None


class ServersDAO(BaseDAO):
    model = Servers

    @classmethod
    async def get_server_info(cls, session: AsyncSession,
                              location: str=None,
                              server_id: Union[str, UUID]=None) -> Optional[Servers]:
        try:
            query = None
            if location:
                query = select(cls.model).where(cls.model.location == location)
            elif server_id:
                query = select(cls.model).where(cls.model.server_id == server_id)

            if query is not None:
                result = await session.execute(query)
                return result.unique().scalar_one_or_none()
            else:
                return None

        except Exception as e:
            logger.error(e)
            return None


class ConnectionsDAO(BaseDAO):
    model = Connections

    @classmethod
    async def get_connection_info(cls, session: AsyncSession,
                                  user_id: Union[str, UUID]) -> Optional[Connections]:
        try:
            query = select(cls.model).where(cls.model.user_id == user_id)
            result = await session.execute(query)

            return result.unique().scalar_one_or_none()

        except Exception as e:
            logger.error(e)
            return None