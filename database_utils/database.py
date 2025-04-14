from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncEngine
from config import DatabaseSettings

DATABASE_URL = DatabaseSettings.get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


def connection(method):

    """Асинхронный декоратор для автоматического создания сессии
    В случае ошибки при выполнении делает откат session.rollback()"""

    async def wrapper(*args, **kwargs):
        # Автоматическое открытие и закрытие (после выполнения) сессии
        async with async_session_maker() as session:
            try:
                return await method(*args, **kwargs, session=session)
            except Exception as e:
                # Откат сессии
                await session.rollback()
                raise e

    return wrapper


async def create_tables(engine_: AsyncEngine = engine):
    try:
        async with engine_.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as e:
        raise e