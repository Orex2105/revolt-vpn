from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncEngine
from config import DatabaseSettings
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='db.add')

DATABASE_URL = DatabaseSettings.get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


async def create_tables(engine_: AsyncEngine = engine):
    try:
        async with engine_.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as e:
        logger.error(e)