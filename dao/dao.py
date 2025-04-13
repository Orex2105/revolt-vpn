from dao.base import BaseDAO
from database_utils.models import Users, Servers, Connections
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, Optional
import datetime
from uuid import uuid5, NAMESPACE_DNS, UUID


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add_user(cls,
                       session: AsyncSession,
                       user_tg_id: Union[str, int],
                       created_at: Optional[datetime] = None,
                       expires_at: Optional[datetime] = None,
                       is_active: Optional[bool] = None,
                       was_ever_active: Optional[bool] = None,
                       last_seen: Optional[datetime] = None,
                       subscription_purchase_count: Optional[int] = None,
                       notes: Optional[str] = None) -> UUID:

        """user_tg_id - tg id пользователя (будет преобразован в uuid5)\n
        session - объект класса AsyncSession\n
        created_at - дата создания записи о пользователе (записывается автоматические)\n
        expires_at - дата окончания подписки (по умолчанию Null)\n
        is_active - boolean со статусом подписки (по умолчанию False)\n
        was_ever_active - boolean, означает была-ли когда-то актива подписка (по умолчанию False)\n
        last_seen - дата последнего запроса ключа по подписке (по умолчанию Null)\n
        subscription_purchase_count - количество раз покупки подписки\n
        notes - комментарии по пользователю для админа (по умолчанию Null)"""

        user_id = uuid5(NAMESPACE_DNS, str(user_tg_id))

        await cls.add(
            session,
            user_id=user_id,
            created_at=created_at,
            expires_at=expires_at,
            is_active=is_active,
            was_ever_active=was_ever_active,
            last_seen=last_seen,
            subscription_purchase_count=subscription_purchase_count,
            notes=notes
        )
        return user_id


class ServersDAO(BaseDAO):
    model = Servers


class ConnectionsDAO(BaseDAO):
    model = Connections