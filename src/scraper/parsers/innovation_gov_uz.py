import asyncio
import aiohttp

from datetime import datetime
from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Database
from .base import BaseParser
from ..data.data_storage import DataStorage


class InnovationGovUzParser(BaseParser):
    name = "innovation.gov.uz"

    def _load_attrs(self, category: str, url: str, language: str):
        self.category: str = category
        self.url: str = url
        self.language: str = language

    async def fetch_data(self):
        url = self.url

        headers = {"Accept-Language": self.language}

        try:
            async with ClientSession(trust_env=True, headers=headers) as session:
                async with session.get(url, ssl=False) as response:
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
            datetime_object = datetime.fromisoformat(data['pub_date']).replace(microsecond=0, tzinfo=None)

            result.append(
                {
                    "title": data['title'],
                    "url": f"https://{self.name}/news/" + data['slug'],
                    "image_url": data['image']['file'],
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

