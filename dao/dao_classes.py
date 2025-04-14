from dao.base_dao import BaseDAO
from database_utils.models import Users, Servers, Connections
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, Union
from uuid import uuid5, NAMESPACE_DNS


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> Sequence[Users]:
        query = select(cls.model)
        result = await session.execute(query)

        # Извлекаем записи как объекты модели
        records = result.unique().scalars().all()
        return records


    @classmethod
    async def get_user_info(cls, session: AsyncSession, user_tg_id: Union[str, int]) -> Users:
        user_uuid = uuid5(NAMESPACE_DNS, str(user_tg_id))
        query = select(cls.model).where(cls.model.user_id == user_uuid)
        result = await session.execute(query)

        return result.unique().scalar_one_or_none()


class ServersDAO(BaseDAO):
    model = Servers

    @classmethod
    async def get_server_info(cls, session: AsyncSession, server_id: str) -> Servers:
        query = select(cls.model).where(cls.model.server_id == server_id)
        result = await session.execute(query)

        return result.unique().scalar_one_or_none()


class ConnectionsDAO(BaseDAO):
    model = Connections

    @classmethod
    async def get_connection_info(cls, session: AsyncSession, user_tg_id: Union[str, int]) -> Connections:
        user_uuid = uuid5(NAMESPACE_DNS, str(user_tg_id))
        query = select(cls.model).where(cls.model.user_id == user_uuid)
        result = await session.execute(query)

        return result.unique().scalar_one_or_none()