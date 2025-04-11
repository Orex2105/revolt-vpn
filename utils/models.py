from sqlalchemy import TEXT, INTEGER, UUID, TIMESTAMP, BOOLEAN, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import datetime
from utils.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True)

    # Связь с таблицой Connections, back_populates - двустороння связь
    connections: Mapped[list["Connections"]] = relationship("Connections", back_populates="user")


class Servers(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    server_id: Mapped[uuid.UUID] = mapped_column(UUID, unique=True)
    server_name: Mapped[str] = mapped_column(TEXT)
    address: Mapped[str] = mapped_column(TEXT)
    port: Mapped[int] = mapped_column(INTEGER, default=443)

    # Связь с таблицой Connections
    connections: Mapped[list["Connections"]] = relationship("Connections", back_populates="server")


class Connections(Base):
    __tablename__ = 'connections'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    server_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("servers.server_id"))
    client_uuid: Mapped[uuid.UUID] = mapped_column(UUID)
    flow: Mapped[str] = mapped_column(TEXT)
    tag: Mapped[str] = mapped_column(TEXT, default='ANARCHY-VPN')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())

    # Связь с таблицой Users
    user: Mapped["Users"] = relationship("Users", back_populates="connections")
    # Связь с таблицой Servers
    server: Mapped["Servers"] = relationship("Servers", back_populates="connections")


class ArchivedConnections(Base):
    __tablename__ = 'archived_connections'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    server_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("servers.server_id"))
    client_uuid: Mapped[uuid.UUID] = mapped_column(UUID)
    flow: Mapped[str] = mapped_column(TEXT)
    tag: Mapped[str] = mapped_column(TEXT, default='ANARCHY-VPN')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    archived_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())