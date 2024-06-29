import asyncio
import aiohttp
import locale

from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from bs4 import BeautifulSoup, Tag
from .base import BaseParser
from ..data.data_storage import DataStorage
from src.db.database import Database


class XsUzParser(BaseParser):
    name = "xs.uz"

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
        # Set the locale to Uzbek
        locale.setlocale(locale.LC_TIME, 'uz_UZ.UTF-8')
        date_obj = datetime.strptime(date_str, '%H:%M %d %B %Y')

        return date_obj
                
    def parse_data(self, raw_data):
        soup = BeautifulSoup(raw_data, 'html.parser')
        all_data = soup.find('div', class_=['news-items-l'])

        result = []

        for data in all_data:
            if isinstance(data, Tag):
                media_body = data.find('div', class_='media-body')
                title = media_body.find('a').get_text()
                url = 'https://xs.uz' + media_body.find('a')['href']

                date_str = media_body.find('span', class_='date').get_text()
                datetime_object = self.__extract_date_from_str(date_str)

                if datetime_object:
                    result.append(
                        {
                            "title": title,
                            "url": url,
                            "image_url": None,
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

