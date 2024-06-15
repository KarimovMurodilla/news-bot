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


class DaryoUzParser(BaseParser):
    name = "daryo.uz"

    def _load_attrs(self, category, url, language):
        self.category = category
        self.url = url
        self.language = language
    
    def __extract_date_from_url(self, url: str):
        match = re.search(r'/(\d{4}/\d{2}/\d{2})/', url)
        if match:
            date_str = match.group(1)
            
            date_obj = datetime.strptime(date_str, "%Y/%m/%d")
            return date_obj
        else:
            print("Date not found in URL")

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
        all_data = soup.find('div', class_=['loop'])
    
        result = []

        for data in all_data:
            if isinstance(data, Tag):
                content = data.find('div', class_='content')
                title = content.find('h2', class_="is-title")
                url = content.find('a')['href']
                datetime_object = self.__extract_date_from_url(url)
                
                result.append(
                    {
                        "title": title.get_text(strip=True),
                        "url": f"https://{self.name}" + url,
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

