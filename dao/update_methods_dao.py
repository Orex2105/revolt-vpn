from dao.dao_classes import UsersDAO
from database_utils.database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from uuid import UUID


@connection
async def update_last_seen(session: AsyncSession, user_id: Union[str, UUID]) -> bool:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param user_id: str или UUID id пользователя
    :return: True в случае успеха и False в случае ошибки
    """

    return await UsersDAO.update_last_seen(session=session, user_id=user_id)