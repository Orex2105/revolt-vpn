import asyncio
from pydantic_models.models import ServerIsAlive
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

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