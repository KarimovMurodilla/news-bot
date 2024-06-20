"""User model file."""
import datetime
import sqlalchemy as sa

from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    """User model."""

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False, primary_key=True
    )
    """ Telegram user id """
    user_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram user name """
    first_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram profile first name """
    second_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    language: Mapped[str] = mapped_column(
        sa.VARCHAR(50), unique=False, nullable=True
    )
    """ Telegram profile second name """
    is_premium: Mapped[bool] = mapped_column(
        sa.Boolean, unique=False, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        sa.Boolean, unique=False, nullable=True
    )
    """ Telegram user premium status """
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return f"{self.first_name}"
