from dao.dao_classes import UsersDAO, ConnectionsDAO
from database_utils.database import connection
from database_utils.models import  Users, Connections
from typing import Union


@connection
async def get_user_info(session, user_tg_id: Union[str, int]) ->  Users:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param user_tg_id: str или int tg id пользователя
    :return: объект класса Users
    """
    return await UsersDAO.get_user_info(session, user_tg_id)


@connection
async def get_connection_info(session, user_tg_id: Union[str, int]) -> Connections:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param user_tg_id: str или int tg id пользователя
    :return: объект класса Connections
    """
    return await ConnectionsDAO.get_connection_info(session, user_tg_id)