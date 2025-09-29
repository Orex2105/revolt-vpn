from database_utils.database import async_session_maker
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='utils.decorators.Connection')


def connection(method):
    """Асинхронный декоратор для автоматического создания сессии\n
    В случае ошибки при выполнении делает откат session.rollback()"""
    async def wrapper(*args, **kwargs):
        try:
        # Автоматическое открытие и закрытие (после выполнения) сессии
            async with async_session_maker() as session:
                try:
                    return await method(*args, **kwargs, session=session)
                except Exception as e:
                    # Откат сессии
                    await session.rollback()
                    logger.error(e)
        except Exception as e:
            logger.error(e)

    return wrapper