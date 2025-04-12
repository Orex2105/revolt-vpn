from sqlalchemy.ext.asyncio import AsyncSession
from utils.database import connection
from utils.models import Users, Servers, Connections
from typing import Union, Optional
import datetime
from uuid import uuid5, NAMESPACE_DNS, UUID


@connection
async def add_user(user_tg_id: Union[str, int],
                   session: AsyncSession,
                   created_at: Optional[datetime] = None,
                   expires_at: Optional[datetime] = None,
                   is_active: Optional[bool] = None,
                   was_ever_active: Optional[bool] = None,
                   last_seen: Optional[datetime] = None,
                   notes: Optional[str] = None) -> UUID:

    """user_tg_id - tg id пользователя (будет преобразован в uuid5)
    session - объект класса AsyncSession (создается в декораторе @connection)
    created_at - дата создания записи о пользователе (записывается автоматические)
    expires_at - дата окончания подписки (по умолчанию Null)
    is_active - boolean со статусом подписки (по умолчанию False)
    was_ever_active - boolean, означает была-ли когда-то актива подписка (по умолчанию False)
    last_seen - дата последнего запроса ключа по подписке (по умолчанию Null)
    notes - комментарии по пользователю для админа (по умолчанию Null)"""

    user_id = uuid5(NAMESPACE_DNS, str(user_tg_id))

    new_user = Users(user_id = user_id,
                     created_at = created_at,
                     expires_at = expires_at,
                     is_active = is_active,
                     was_ever_active = was_ever_active,
                     last_seen = last_seen,
                     notes = notes)
    # Объект session создается в декораторе @connection
    session.add(new_user)
    await session.commit()
    return user_id