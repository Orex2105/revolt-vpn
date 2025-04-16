from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


class BaseDAO:

    """Базовый класс для Data Access Object-классов, которые
    будут создаваться для каждой таблицы"""

    model = None

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        new_record = cls.model(**values)
        session.add(new_record)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(e)

        return new_record