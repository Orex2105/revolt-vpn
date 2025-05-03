import asyncio
import logging

logger = logging.getLogger(__name__)

async def is_alive(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception as e:
        logger.error(e)
        return False
