"""User repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Category
from .abstract import Repository


class CategoryRepo(Repository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Category, session=session)

    async def new(
        self,
        name: str
    ) -> None:
        await self.session.merge(
            Category(
                name=name
            )
        )
        await self.session.commit()

    async def get_by_name(self, name: str) -> Category:
        return await self.session.scalar(
            select(Category).where(Category.name == name).limit(1)
        )
