"""User model file."""
import datetime
import sqlalchemy as sa

from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Url(Base):
    url: Mapped[str] = mapped_column(
        sa.Text, unique=True, nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        sa.ForeignKey('category.id', ondelete='CASCADE'),
        unique=False,
        nullable=False,
    )
    source_id: Mapped[int] = mapped_column(
        sa.ForeignKey('source.id', ondelete='CASCADE'),
        unique=False,
        nullable=False,
    )
    language: Mapped[str] = mapped_column(
        sa.VARCHAR(50), unique=False, nullable=True
    )
    created_at: Mapped[Optional[Annotated[
        datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)
    ]]]

    def __str__(self):
        return f"{self.url}"
