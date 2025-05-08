from dao.dao_classes import UserDAO, ServerDAO, CountryDAO, SubscriptionDAO, AdminDAO
from database_utils.models import User, Server, Country, Subscription, Admin
from utils.decorators.connection import connection
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@connection
async def add_user(session: AsyncSession,
                   telegram_id: int) -> Optional[User]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param telegram_id: Telegram ID пользователя
    :return: Optional[User]
    """
    try:

        new_user = await UserDAO.add(
            session=session,
            telegram_id=telegram_id,
        )
        return new_user

    except Exception as e:
        logger.error(e)
        return None


@connection
async def add_server(session: AsyncSession,
                     country_id: int,
                     ip_address: str,
                     port: int = 4443,
                     description: Optional[str] = None,
                     is_active: bool = True) -> Optional[Server]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param country_id: ID страны (внешний ключ на таблицу Country)
    :param ip_address: IP-адрес или домен сервера
    :param port: порт сервера (по умолчанию 4443)
    :param description: описание сервера
    :param is_active: активен ли сервер
    :return: Optional[Server]
    """
    try:
        new_server = await ServerDAO.add(
            session=session,
            country_id=country_id,
            ip_address=ip_address,
            port=port,
            description=description,
            is_active=is_active
        )
        return new_server

    except Exception as e:
        logger.error(e)
        return None


@connection
async def add_admin(session: AsyncSession,
                    name: str,
                    telegram_id: int) -> Optional[Admin]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param name: имя администратора
    :param telegram_id: Telegram ID администратора
    :return: Optional[Admin]
    """
    try:
        new_admin = await AdminDAO.add(
            session=session,
            name=name,
            telegram_id=telegram_id
        )
        return new_admin
    except Exception as e:
        logger.error(e)
        return None


@connection
async def add_subscription(session: AsyncSession,
                           telegram_id: int,
                           duration_days: int = 30,
                           start_date: Optional[datetime] = datetime.now()) -> Optional[Subscription]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param telegram_id: Telegram ID пользователя
    :param duration_days: длительность подписки в днях (по умолчанию 30)
    :param start_date: дата начала подписки
    :return: Optional[Subscription]
    """
    try:
        if not start_date:
            start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)

        new_subscription = await SubscriptionDAO.add(
            session=session,
            telegram_id=telegram_id,
            start_date=start_date,
            end_date=end_date
        )
        return new_subscription
    except Exception as e:
        logger.error(e)
        return None


@connection
async def add_country(session: AsyncSession,
                      name: str,
                      code: str) -> Optional[Country]:
    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param name: название страны
    :param code: код страны (RU, UK...)
    :return: Optional[Country]
    """
    try:
        new_country = await CountryDAO.add(
            session=session,
            name=name,
            code=code
        )
        return new_country
    except Exception as e:
        logger.error(e)
        return None