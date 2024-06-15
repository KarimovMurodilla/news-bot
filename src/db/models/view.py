"""User model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class View(Base):
    """View model."""
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey('user.user_id', ondelete='CASCADE'),
        unique=False,
        nullable=False,
    )
    news_id: Mapped[int] = mapped_column(
        sa.ForeignKey('news.id', ondelete='CASCADE'),
        unique=False,
        nullable=False,
    )
    created_at: Mapped[Optional[Annotated[
        datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)
    ]]]

    def __str__(self):
        return f"{self.user_id}"
