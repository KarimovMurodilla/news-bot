"""User repository file."""
import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import News
from .abstract import Repository


class NewsRepo(Repository[News]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=News, session=session)

    async def new(
        self,
        title: str,
        url: str,
        image_url: str,
        category: int,
        source: int,
        language: str,
        date: str,
        formatted_date: str
    ) -> None:
        await self.session.merge(
            News(
                title=title,
                url=url,
                image_url=image_url,
                category_id=category,
                source_id=source,
                language=language,
                date=date,
                formatted_date=formatted_date
            )
        )
        await self.session.commit()

    async def get_by_url(self, url: str) -> News:
        """Get user role by id."""
        return await self.session.scalar(
            select(News).where(News.url == url).limit(1)
        )

    async def get_all_by_category(self, category_id: int):
        """Get user role by id."""
        result = await self.session.scalars(
            select(News)
            .where(News.category_id == category_id)
            .order_by(News.date.desc())
        )
        return result.all()
    
    async def get_recent_news_last_15_minutes(self):
        # Calculate the time 30 minutes ago from now
        thirty_minutes_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
        
        stmt = select(News).where(News.created_at >= thirty_minutes_ago).order_by(News.date.desc())
        result = await self.session.execute(stmt)        
        news_list = result.scalars().all()
        
        return news_list

    async def get_recent_news(self, language: str, category_id: int):
        last_24_hours = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        
        stmt = (
            select(News)
            .filter(News.language == language)
            .filter(News.category_id == category_id)
            .filter(News.created_at >= last_24_hours)
        )
        
        result = await self.session.execute(stmt)
        news_items = result.scalars().all()
        
        return news_items
