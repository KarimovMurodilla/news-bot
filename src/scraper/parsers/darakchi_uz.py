import re
import asyncio
import aiohttp

from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from bs4 import BeautifulSoup, Tag
from .base import BaseParser
from ..data.data_storage import DataStorage
from src.db.database import Database


class DarakchiUzParser(BaseParser):
    name = "darakchi.uz"

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
        all_data = soup.find_all('div', class_=['col-md-6 col-lg-4 mb-3'])

        result = []

        for data in all_data:
            if isinstance(data, Tag):
                card_body = data.find('div', class_="card-body")
                a_tag = card_body.find('a')
                url = a_tag['href']
                title = a_tag.get_text(strip=True)

                card_text = card_body.find('p', class_="card-text")
                date = card_text.get_text(strip=True)
                datetime_object = datetime.strptime(date, "%d.%m.%Y, %H:%M")

                card = data.find('div', class_="card")
                image_url = card.find('img', class_="img-fluid")['src']

                result.append(
                    {
                        "title": title,
                        "url": url,
                        "image_url": image_url,
                        "source": self.name,
                        "category": self.category,
                        "date": datetime_object,
                        "language": self.language,
                        "formatted_date": self.format_date(str(datetime_object))
                    }
                )

        return result

    async def save_data(self, parsed_data):
        async with AsyncSession(self.engine) as session:
            db = Database(session)
            data_store = DataStorage()
            await data_store.save_to_db(db, parsed_data)

