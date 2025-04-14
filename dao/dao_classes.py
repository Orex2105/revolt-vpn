from dao.base_dao import BaseDAO
from database_utils.models import Users, Servers, Connections
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        query = select(cls.model)
        result = await session.execute(query)

        # Извлекаем записи как объекты модели
        records = result.unique().scalars().all()
        return records


class ServersDAO(BaseDAO):
    model = Servers


class ConnectionsDAO(BaseDAO):
    model = Connections