from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Url
from .abstract import Repository


class UrlRepo(Repository[Url]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Url, session=session)

    async def new(
        self,
        url: str,
        category_id: int,
        source_id: int
    ) -> None:
        await self.session.merge(
            Url(
                url=url,
                category_id=category_id,
                source_id=source_id
            )
        )
        await self.session.commit()

    async def get_by_source(self, source_id: int) -> List[Url]:
        result = await self.session.scalars(
            select(Url).where(Url.source_id == source_id)
        )
        return result.all()
