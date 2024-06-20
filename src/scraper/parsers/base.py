# parsers/base_parser.py
import locale
import aiohttp

from sqlalchemy.ext.asyncio import AsyncSession

from src.configuration import conf
from src.db.database import Database
from src.db.database import create_async_engine
from src.misc.cosine_similarity import calculate

from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class BaseParser(ABC):
    name = None

    def __init__(self):
        self.engine = create_async_engine(url=conf.db.build_connection_str())

    @abstractmethod
    async def fetch_data(self):
        """Fetch raw data from the specified URL"""
        pass

    @abstractmethod
    def parse_data(self, raw_data):
        """Parse the fetched raw data"""
        pass

    @abstractmethod
    async def save_data(self, parsed_data):
        """Save the parsed data to a desired location"""
        pass

    @abstractmethod
    async def _load_attrs(self):
        pass

    async def run(self):
        """Run the complete parsing process"""
        async with aiohttp.ClientSession() as session:
            raw_data = await self.fetch_data(session)
            parsed_data = self.parse_data(raw_data)
            self.save_data(parsed_data)

        return parsed_data

    async def filter_recent_news(self):
        raw_data = await self.fetch_data()
        parsed_data = self.parse_data(raw_data)
    
        now = datetime.now()
        today = now.date()
        yesterday = today - timedelta(days=1)

        recent_news = []
        for item in parsed_data:
            item_date = datetime.strptime(str(item['date']), "%Y-%m-%d %H:%M:%S").date()
            if item_date == today or item_date == yesterday:
                recent_news.append(item)
                
        await self.save_data(recent_news)
        return recent_news
    
    def format_date(self, date_str):
        locale.setlocale(locale.LC_TIME, 'uz_UZ.UTF-8')
        
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        formatted_date = date_obj.strftime("%B %d, %Y, %H:%M")
        return formatted_date

    async def parse_all_and_save(self):
        async with AsyncSession(self.engine) as session:
            db = Database(session)
            source = await db.source.get_by_url(self.name)
            urls = await db.url.get_by_source(source_id=source.id)
            
            for url in urls:
                category = await db.category.get(url.category_id)

                self._load_attrs(category=category.name, url=url.url, language=url.language)

                raw_data = await self.fetch_data()
                parsed_data = self.parse_data(raw_data)

                recent_news = await db.news.get_recent_news(url.language, url.category_id)

                # try:
                for data in parsed_data:
                    news = await db.news.get_by_url(data['url'])
                
                    if not news:
                        can_save = True
                        for new in recent_news:
                            similarity = calculate(new.title, data['title'])
                            if similarity > 0.5:
                                can_save = False
                                break
                            
                        if can_save:
                            print("----------Saved---------")
                            await self.save_data(data)
                # except Exception as e:
                #     print(e)
