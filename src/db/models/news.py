"""User model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from src.misc.cosine_similarity import calculate

from .base import Base


class News(Base):
    """News model."""
    title: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    url: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    image_url: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
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
    date: Mapped[str] = mapped_column(
        sa.DateTime, unique=False, nullable=True
    )
    formatted_date: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    language: Mapped[str] = mapped_column(
        sa.VARCHAR(50), unique=False, nullable=True
    )  
    created_at: Mapped[Optional[Annotated[
        datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)
    ]]]

    def __str__(self):
        return f"{self.url}"

    def __eq__(self, other):
        same_url = self.url == other['url']
        similarity = calculate(self.title, other['title'])
        # print('Db data:', self.title)
        # print('Parsed data:', other['title'])
        # print("Similarity:", similarity)
        return same_url or similarity >= 0.5 
