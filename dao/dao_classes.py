from dao.base_dao import BaseDAO
from database_utils.models import Users, Servers, Connections
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, Union, Optional
from uuid import UUID


class UsersDAO(BaseDAO):
    model = Users

    @classmethod # Вопрос: оставить или удалить?
    async def get_all_users(cls, session: AsyncSession) -> Sequence[Users]:
        # Формируем запрос
        query = select(cls.model)
        result = await session.execute(query)

        # Извлекаем записи как объекты модели
        records = result.unique().scalars().all()
        return records


    @classmethod
    async def get_user_info(cls, session: AsyncSession,
                            user_id: Union[str, UUID]) -> Optional[Users]:
        query = select(cls.model).where(cls.model.user_id == user_id)
        result = await session.execute(query)

        return result.unique().scalar_one_or_none()


class ServersDAO(BaseDAO):
    model = Servers

    @classmethod
    async def get_server_info(cls, session: AsyncSession,
                              location: str=None,
                              server_id: Union[str, UUID]=None) -> Optional[Servers]:
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


class ConnectionsDAO(BaseDAO):
    model = Connections

    @classmethod
    async def get_connection_info(cls, session: AsyncSession,
                                  user_id: Union[str, UUID]) -> Optional[Connections]:
        query = select(cls.model).where(cls.model.user_id == user_id)
        result = await session.execute(query)

        return result.unique().scalar_one_or_none()