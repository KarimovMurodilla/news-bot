"""User repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import View
from .abstract import Repository


class ViewRepo(Repository[View]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=View, session=session)

    async def new(
        self,
        name: str
    ) -> None:
        await self.session.merge(
            View(
                name=name
            )
        )
        await self.session.commit()

    async def get_me(self, id: int) -> View:
        """Get user role by id."""
        return await self.session.scalar(
            select(View).where(View.id == id).limit(1)
        )
