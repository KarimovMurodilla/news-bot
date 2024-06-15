"""User model file."""
import datetime
import sqlalchemy as sa

from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Category(Base):
    """Category model."""
    name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )

    def __str__(self):
        return f"{self.name}"
