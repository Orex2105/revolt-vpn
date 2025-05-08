from dao.base_dao import BaseDAO
from database_utils.models import User, Subscription, Country, Server, Admin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def user_info(cls, session: AsyncSession, telegram_id: int) -> Optional[User]:
        try:
            query = select(cls.model).where(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
        except Exception as e:
            logger.error(e)
            return None


class SubscriptionDAO(BaseDAO):
    model = Subscription

    @classmethod
    async def subscription_info(cls, session: AsyncSession, telegram_id: int) -> Optional[Subscription]:
        try:
            query = select(cls.model).where(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
        except Exception as e:
            logger.error(e)
            return None


class AdminDAO(BaseDAO):
    model = Admin

    @classmethod
    async def all_admins(cls, session: AsyncSession) -> Optional[list[int]]:
        try:
            query = select(cls.model)
            result = await session.execute(query)
            admins = result.unique().scalars().all()
            return [admin.telegram_id for admin in admins]
        except Exception as e:
            logger.error(e)
            return None

    @classmethod
    async def admin_info(cls, session: AsyncSession, telegram_id: int) -> Optional[Admin]:
        try:
            query = select(cls.model).where(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
        except Exception as e:
            logger.error(e)
            return None


class CountryDAO(BaseDAO):
    model = Country

    @classmethod
    async def country_info(cls, session: AsyncSession, country_id: int) -> Optional[Country]:
        try:
            query = select(cls.model).where(cls.model.id == country_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
        except Exception as e:
            logger.error(e)
            return None

    @classmethod
    async def all_countries(cls, session: AsyncSession) -> Optional[list[Country]]:
        try:
            query = select(cls.model)
            result = await session.execute(query)
            return list(result.unique().scalars().all())
        except Exception as e:
            logger.error(e)
            return None


class ServerDAO(BaseDAO):
    model = Server

    @classmethod
    async def all_servers(cls, session: AsyncSession) -> Optional[list[Server]]:
        try:
            query = select(cls.model)
            result = await session.execute(query)
            return list(result.unique().scalars().all())
        except Exception as e:
            logger.error(e)
            return None


    @classmethod
    async def server_info(cls, session: AsyncSession, server_id: int) -> Optional[Server]:
        try:
            query = select(cls.model).where(cls.model.id == server_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
        except Exception as e:
            logger.error(e)
            return None