# parsers/base_parser.py
import locale
import logging
import traceback

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
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

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
    async def save_data(self, data):
        """Save the parsed data to a desired location"""
        pass

    @abstractmethod
    async def _load_attrs(self):
        pass
    
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
            
            try:
                for url in urls:
                    category = await db.category.get(url.category_id)

                    self._load_attrs(category=category.name, url=url.url, language=url.language)

                    self.logger.info("Request to url: " + url.url)

                    raw_data = await self.fetch_data()
                    parsed_data = self.parse_data(raw_data)
                    recent_news = await db.news.get_recent_news()

                    for data in parsed_data:
                        date_to_check: datetime = data['date']
                        is_today = datetime.now().date() == date_to_check.date()

                        if is_today:
                            if data not in recent_news:                                
                                await self.save_data(data)
                                self.logger.info("+++Saved+++: " + data['title'])
                        else:
                            self.logger.warning("---Old new. Not saved---: " + data['title'])
            except Exception as e:
                traceback.print_exc()
                print(e)
