import asyncio
from pydantic_models.models import ServerIsAlive
from datetime import datetime
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='utils.Ping')


async def is_alive(host: str, port: int, timeout: float = 1.0) -> ServerIsAlive:
    current_time = datetime.now().strftime("%H:%M")
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        writer.close()
        await writer.wait_closed()

        return ServerIsAlive(status=True, last_check=current_time)

    except Exception as e:
        logger.error(e)
        return ServerIsAlive(status=False, last_check=current_time)