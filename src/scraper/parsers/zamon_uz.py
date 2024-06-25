import asyncio
import aiohttp
from datetime import datetime

from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Database
from .base import BaseParser
from ..data.data_storage import DataStorage


class ZamonUzParser(BaseParser):
    name = "zamon.uz"

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
                        return await response.json()
                    else:
                        raise Exception(f"Failed to fetch data from {url}")
        except ClientConnectorError as e:
            print(f"Attempt failed: {e}")
            await asyncio.sleep(1)
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
                
    def parse_data(self, raw_data):
        all_data = raw_data['results']
    
        result = []

        for data in all_data:
            datetime_with_tz = datetime.fromisoformat(data['pub_date'])
            datetime_object = datetime_with_tz.replace(tzinfo=None)

            result.append(
                {
                    "title": data['title'],
                    "url": f"https://{self.name}/detail/" + data['url'],
                    "image_url": data['image']['original'],
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

