"""User model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Source(Base):
    """Category model."""
    url: Mapped[str] = mapped_column(
        sa.Text, unique=True, nullable=True
    )
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return f"{self.url}"
