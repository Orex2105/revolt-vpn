from dao.dao_classes import UsersDAO, ServersDAO, ConnectionsDAO
from database_utils.database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, Optional
from uuid import uuid5, UUID, NAMESPACE_DNS
from datetime import datetime
from database_utils.models import Users, Servers, Connections
import asyncio


@connection
async def add_user(session: AsyncSession,
                   user_tg_id: Union[str, int],
                   created_at: Optional[datetime] = None,
                   expires_at: Optional[datetime] = None,
                   is_active: Optional[bool] = None,
                   was_ever_active: Optional[bool] = None,
                   last_seen: Optional[datetime] = None,
                   subscription_purchase_count: Optional[int] = None,
                   notes: Optional[str] = None) -> Users:

    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param user_tg_id: tg id пользователя (будет преобразован в uuid5)
    :param created_at: дата создания записи о пользователе (записывается автоматические)
    :param expires_at: дата окончания подписки (по умолчанию Null)
    :param is_active: boolean со статусом подписки (по умолчанию False)
    :param was_ever_active: boolean, означает была-ли когда-то актива подписка (по умолчанию False)
    :param last_seen: дата последнего запроса ключа по подписке (по умолчанию Null)
    :param subscription_purchase_count: количество раз покупки подписки
    :param notes: комментарии по пользователю для админа (по умолчанию Null)
    :return: объект класса Users
    """

    user_id = uuid5(NAMESPACE_DNS, str(user_tg_id))

    new_user = await UsersDAO.add(
        session=session,
        user_id=user_id,
        created_at=created_at,
        expires_at=expires_at,
        is_active=is_active,
        was_ever_active=was_ever_active,
        last_seen=last_seen,
        subscription_purchase_count=subscription_purchase_count,
        notes=notes
    )
    return new_user


@connection
async def add_new_server(session: AsyncSession,
                         location: str,
                         address: str,
                         port: int,
                         panel_url: str,
                         server_id: Optional[UUID] = None
                         ) -> Servers:

    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param location: название локации
    :param address: ip-адрес сервера или его домен
    :param port: порт для подключения к серверу
    :param panel_url: ссылка на панель управления
    :param server_id: uuid сервера
    :return: объект класса Servers
    """

    if not server_id:
        server_id = uuid5(NAMESPACE_DNS, location)

    new_server = await ServersDAO.add(
        session=session,
        server_id=server_id,
        location=location.lower(),
        address=address,
        port=port,
        panel_url=panel_url
    )
    return new_server


@connection
async def add_new_connection(session: AsyncSession,
                             user_tg_id: Union[str, int],
                             server_id: UUID,
                             flow: Optional[str] = None,
                             tag: str = None,
                             created_at: Optional[datetime] = None,
                             is_archived: Optional[bool] = None,
                             archived_at: Optional[datetime] = None
                             ) -> Connections:

    """
    :param session: объект класса AsyncSession (создается декоратором)
    :param user_tg_id: tg id пользователя (будет преобразован в uuid5)
    :param server_id: uuid сервера
    :param flow: механизм управления трафиком (по умолчанию xtls-rprx-vision)
    :param tag: тэг для ключа подключения (по умолчанию Null)
    :param created_at: дата создания записи о подключении (задается при создании записи)
    :param is_archived: boolean состояния ключа (действует или архив)
    :param archived_at: дата архивации (по умолчанию Null)
    :return: объект класса Connections
    """

    user_id = uuid5(NAMESPACE_DNS, str(user_tg_id))

    new_connection = await ConnectionsDAO.add(
        session=session,
        user_id=user_id,
        server_id=server_id,
        flow=flow,
        tag=tag,
        created_at=created_at,
        is_archived=is_archived,
        archived_at=archived_at
    )
    return new_connection


t1 = asyncio.run(add_new_connection(user_tg_id=123,
                                   server_id='b501803a-c891-55cd-abec-b69a184b6307'))