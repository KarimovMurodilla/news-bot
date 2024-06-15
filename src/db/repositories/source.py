"""User repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Source
from .abstract import Repository


class SourceRepo(Repository[Source]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Source, session=session)

    async def new(
        self,
        url: str
    ) -> None:
        await self.session.merge(
            Source(
                url=url
            )
        )
        await self.session.commit() 

    async def get_by_url(self, url: str) -> Source:
        return await self.session.scalar(
            select(Source).where(Source.url == url).limit(1)
        )
