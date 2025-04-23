from typing import Optional
from sqlalchemy import TEXT, INTEGER, UUID, TIMESTAMP, BOOLEAN, func, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import datetime
from database_utils.database import Base


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), index=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=False, index=True)
    was_ever_active: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    last_seen: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    subscription_purchase_count: Mapped[int] = mapped_column(INTEGER, default=0)
    notes: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    # Связь с таблицей Connections
    connections: Mapped["Connections"] = relationship("Connections",
                                                      back_populates="user", lazy="joined")
    admin: Mapped["Admins"] = relationship("Admins", back_populates="user", lazy="joined")


class Admins(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(TEXT, unique=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))

    user: Mapped["Users"] = relationship("Users", back_populates="admin", lazy="joined")


class Servers(Base):
    __tablename__ = "servers"

    server_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    location: Mapped[str] = mapped_column(TEXT)
    address: Mapped[str] = mapped_column(TEXT)
    port: Mapped[int] = mapped_column(INTEGER, default=443)
    panel_url: Mapped[str] = mapped_column(TEXT)

    # Связь с таблицей Connections
    connections: Mapped[list["Connections"]] = relationship("Connections",
                                                          back_populates="server", lazy="joined")


class Connections(Base):
    __tablename__ = 'connections'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), unique=True, index=True)
    server_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("servers.server_id"), index=True)
    flow: Mapped[str] = mapped_column(TEXT, default='xtls-rprx-vision')
    tag: Mapped[str] = mapped_column(TEXT, default='REVOLT-VPN')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    is_archived: Mapped[bool] = mapped_column(BOOLEAN, default=False, index=True)
    archived_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True, index=True)

    # Связь с Users
    user: Mapped["Users"] = relationship("Users", back_populates="connections", lazy="joined")
    # Связь с Servers
    server: Mapped["Servers"] = relationship("Servers", back_populates="connections", lazy="joined")