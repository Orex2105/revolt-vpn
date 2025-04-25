from sqlalchemy.ext.asyncio import AsyncSession
from dao.dao_classes import UsersDAO, AdminsDAO, ConnectionsDAO, ServersDAO
from utils.decorators.connection import connection
from database_utils.models import Users, Admins, Connections, Servers
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
async def get_admin_info(session: AsyncSession,
                        tg_id: int) ->  Optional[Admins]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param tg_id: str tg id пользователя
    :return: объект класса Admins или None
    """
    return await AdminsDAO.get_admin_info(session, tg_id)


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
async def get_servers_locations(session: AsyncSession) -> Optional[list[str]]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :return: список локаций или None
    """
    return await ServersDAO.get_servers_locations(session)


@connection
async def get_connection_info(session: AsyncSession,
                              user_id: Union[str, UUID]) -> Optional[Connections]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param user_id: str или UUID id пользователя
    :return: объект класса Connections или None
    """
    return await ConnectionsDAO.get_connection_info(session, user_id)