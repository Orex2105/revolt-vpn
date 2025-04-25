from uuid import uuid5, UUID, NAMESPACE_DNS


async def hash_uuid5(tg_id: str) -> UUID:
    return uuid5(NAMESPACE_DNS, tg_id)