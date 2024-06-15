from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from src.configuration import conf
from src.db.database import Database
from src.db.database import create_async_engine


class DataStorage:
    async def save(self, db: Database, data: dict):
        title = data['title']
        url = data['url']
        source = await db.source.get_by_url(data['source'])
        category = await db.category.get_by_name(data['category'])
        date = data['date']
        formatted_date = data['formatted_date']
        language = data['language']

        await db.news.new(
            title=title,
            url=url,
            category=category.id,
            source=source.id,
            date=date,
            formatted_date=formatted_date,
            language=language
        )

    async def save_to_db(self, db: Database, all_data: list | dict):
        if isinstance(all_data, list):
            for data in all_data:
                await self.save(db, data)

        elif isinstance(all_data, dict):
            await self.save(db, all_data)
