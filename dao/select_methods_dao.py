from sqlalchemy.ext.asyncio import AsyncSession
from dao.dao_classes import UserDAO, AdminDAO, CountryDAO, ServerDAO, SubscriptionDAO
from utils.decorators.connection import connection
from database_utils.models import User, Admin, Country, Server, Subscription
from typing import Optional
from sqlalchemy import select, func
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='db.SelectDao')


@connection
async def user_info(session: AsyncSession,
                        telegram_id: int) ->  Optional[User]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param telegram_id: Telegram ID пользователя
    :return: Optional[User]
    """
    return await UserDAO.user_info(session=session, telegram_id=telegram_id)


@connection
async def subscription_info(session: AsyncSession, telegram_id: int) -> Optional[Subscription]:
    return await SubscriptionDAO.subscription_info(session=session, telegram_id=telegram_id)


@connection
async def admin_info(session: AsyncSession,
                        telegram_id: int) ->  Optional[Admin]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param telegram_id: Telegram ID пользователя
    :return: Optional[Admin]
    """
    return await AdminDAO.admin_info(session=session, telegram_id=telegram_id)


@connection
async def all_admins(session: AsyncSession) -> Optional[list[int]]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :return: список Telegram ID администраторов
    """
    return await AdminDAO.all_admins(session=session)


@connection
async def server_info(session: AsyncSession,  server_id: int) -> Optional[Server]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param server_id: id сервера
    :return: Optional[Server]
    """
    return await ServerDAO.server_info(session=session, server_id=server_id)


@connection
async def all_servers(session: AsyncSession) -> Optional[list[Server]]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :return: список объектов класса Server
    """
    return await ServerDAO.all_servers(session=session)


@connection
async def country_info(session: AsyncSession, country_id: int) -> Optional[Country]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param country_id: ID страны
    :return: Optional[Country]
    """
    return await CountryDAO.country_info(session=session, country_id=country_id)


@connection
async def all_countries(session: AsyncSession) -> Optional[list[Country]]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :return: список объектов класса Country
    """
    return await CountryDAO.all_countries(session=session)


@connection
async def get_next_id_users(session: AsyncSession):
    result = await session.execute(select(func.max(User.id)))
    max_id = result.scalar()
    return (max_id or 0) + 1


@connection
async def get_next_id_subscriptions(session: AsyncSession):
    result = await session.execute(select(func.max(Subscription.id)))
    max_id = result.scalar()
    return (max_id or 0) + 1