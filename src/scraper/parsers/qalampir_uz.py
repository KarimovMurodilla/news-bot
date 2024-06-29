import asyncio
import aiohttp

from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from .base import BaseParser
from ..data.data_storage import DataStorage
from src.db.database import Database


class QalampirUzParser(BaseParser):
    name = "qalampir.uz"

    def _load_attrs(self, category, url, language):
        self.category = category
        self.url = url
        self.language = language

    async def fetch_data(self):
        url = self.url

        try:
            async with ClientSession(trust_env=True) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        raise Exception(f"Failed to fetch data from {url}")
        except ClientConnectorError as e:
            print(f"Attempt failed: {e}")
            await asyncio.sleep(1)
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def __extract_date_from_str(self, date_str: str):
        # Get the current date and time
        now = datetime.now()

        if len(date_str) == 5:
            date_part = now.date()

            datetime_str = f"{date_part} {date_str}"
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

            return datetime_obj
                
    def parse_data(self, raw_data):
        soup = BeautifulSoup(raw_data, 'html.parser')
        all_data = soup.find('div', id="categories-list")

        result = []
        for data in all_data:
            if isinstance(data, Tag):
                news_card = data.find('a', class_='news-card')
                if news_card:
                    url = news_card['href']
                    title = news_card.find('p', class_='news-card-content-text').get_text(strip=True)

                    image_url = news_card.find('img', class_='news-card-img')['src']

                    date_str = news_card.find('span', class_='date').get_text(strip=True)
                    datetime_object = self.__extract_date_from_str(date_str)

                    if datetime_object:
                        result.append(
                            {
                                "title": title,
                                "url": "https://qalampir.uz" + url,
                                "image_url": image_url,
                                "source": self.name,
                                "category": self.category,
                                "date": datetime_object,
                                "language": self.language,
                                "formatted_date": self.format_date(str(datetime_object))
                            }
                        )
        return result

    async def save_data(self, data):
        async with AsyncSession(self.engine) as session:
            db = Database(session)
            data_store = DataStorage()
            await data_store.save_to_db(db, data)
