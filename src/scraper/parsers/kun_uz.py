import json
import asyncio
import aiohttp

from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from bs4 import BeautifulSoup, Tag
from src.db.database import Database

from .base import BaseParser
from ..data.data_storage import DataStorage


class KunUzParser(BaseParser):
    name = "kun.uz"

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
            
    def parse_data(self, raw_data):
        soup = BeautifulSoup(raw_data, 'html.parser')
        all_data = soup.find('div', class_=['row', 'news'], id="news-list")

        result = []

        for data in all_data:
            if isinstance(data, Tag):
                url = data.find('a')['href']
                title = data.get_text(strip=True)
                index = 18
                if title[6] == '/':
                    date_string = title[:18]
                    datetime_object = datetime.strptime(
                        date_string, "%H:%M / %d.%m.%Y"
                    )
                else:
                    index = 5
                    time_string = title[:5]
                    time_only = datetime.strptime(time_string, "%H:%M")
                    today = datetime.today()
                    datetime_object = today.replace(
                        hour=time_only.hour, minute=time_only.minute, second=0, microsecond=0
                    )
                result.append(
                    {
                        "title": title[index:],
                        "url": f"https://{self.name}" + url,
                        "source": self.name,
                        "category": self.category,
                        "language": self.language,
                        "date": datetime_object,
                        "formatted_date": self.format_date(str(datetime_object))
                    }
                )

        return result

    async def save_data(self, parsed_data):
        async with AsyncSession(self.engine) as session:
            db = Database(session)
            data_store = DataStorage()
            await data_store.save_to_db(db, parsed_data)


