import asyncio
import aiohttp

from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from .base import BaseParser
from ..data.data_storage import DataStorage
from src.db.database import Database


class PresidentUzParser(BaseParser):
    name = "president.uz"

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
        today = datetime.now().date()
        datetime_object = datetime.strptime(date_str, "%d-%m-%Y")

        if today == datetime_object.date():
            datetime_object = datetime.now().replace(microsecond=0)            
            return datetime_object
                
    def parse_data(self, raw_data):
        soup = BeautifulSoup(raw_data, 'html.parser')
        all_data = soup.find_all('div', class_="news_box")

        result = []

        for data in all_data:
            if isinstance(data, Tag):
                text_box = data.find('div', class_='text_box')
                title = text_box.find('a').get_text(strip=True)
                url = text_box.find('a')['href']

                img_box = data.find('div', class_='img_box')
                image_url = img_box.find('img')['src']

                date_str = text_box.find('span', class_='date_text').get_text(strip=True)
                datetime_object = self.__extract_date_from_str(date_str)

                if datetime_object:
                    result.append(
                        {
                            "title": title,
                            "url": f"https://{self.name}" + url,
                            "image_url": f"https://{self.name}" + image_url,
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
