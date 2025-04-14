from dao.dao_classes import UsersDAO
from database_utils.database import connection
from asyncio import run


@connection
async def select_all_users(session):
    return await UsersDAO.get_all_users(session)