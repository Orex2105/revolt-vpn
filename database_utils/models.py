from typing import Optional
from sqlalchemy import TEXT, INTEGER, TIMESTAMP, BOOLEAN, ForeignKey, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database_utils.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription",
                                                               back_populates="user", lazy='joined')
    admin: Mapped[Optional["Admin"]] = relationship("Admin", back_populates="user", lazy='joined')


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(TEXT, unique=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), index=True)

    user: Mapped["User"] = relationship("User", back_populates="admin", lazy='joined')


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False, index=True)
    start_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    end_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, index=True)

    user: Mapped["User"] = relationship("User", back_populates="subscriptions", lazy='joined')


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(TEXT, nullable=False)
    code: Mapped[str] = mapped_column(TEXT, unique=True, nullable=False)

    servers: Mapped[list["Server"]] = relationship("Server", back_populates="country", lazy='joined')


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    ip_address: Mapped[str] = mapped_column(TEXT, nullable=False)
    port: Mapped[int] = mapped_column(INTEGER, default=4443)
    panel_url: Mapped[str] = mapped_column(TEXT)
    description: Mapped[Optional[str]] = mapped_column(TEXT)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True, index=True)
    inbound_id: Mapped[int] = mapped_column(INTEGER, default=1)
    login: Mapped[str] = mapped_column(TEXT)
    password: Mapped[str] = mapped_column(TEXT)

    country: Mapped["Country"] = relationship("Country", back_populates="servers", lazy='joined')