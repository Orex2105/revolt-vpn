from sqlalchemy.ext.asyncio import AsyncSession
from dao.dao_classes import UsersDAO, ConnectionsDAO, ServersDAO
from database_utils.database import connection
from database_utils.models import Users, Connections, Servers
from typing import Union, Optional
from uuid import UUID


@connection
async def get_user_info(session: AsyncSession,
                        user_id: Union[str, UUID]) ->  Optional[Users]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param user_id: str или UUID id пользователя
    :return: объект класса Users или None
    """
    return await UsersDAO.get_user_info(session, user_id)


@connection
async def get_server_info(session: AsyncSession, location: Optional[str]=None,
                          server_id: Union[str, UUID]=None) -> Optional[Servers]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param location: название локации
    :param server_id: uuid сервера
    :return: объект класса Servers или None
    """
    return await ServersDAO.get_server_info(session, location, server_id)


@connection
async def get_connection_info(session: AsyncSession,
                              user_id: Union[str, UUID]) -> Optional[Connections]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param user_id: str или UUID id пользователя
    :return: объект класса Connections или None
    """
    return await ConnectionsDAO.get_connection_info(session, user_id)