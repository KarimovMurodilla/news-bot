import asyncio
import aiohttp

from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from .base import BaseParser
from ..data.data_storage import DataStorage
from src.db.database import Database


class TuitUzParser(BaseParser):
    name = "tuit.uz"

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

    def __extract_date_from_uz_date_str(self, date_str: str):
        res = date_str.split('|')        
        date_part = res[1].strip()
        time_part = res[2].strip()
        datetime_str = f"{date_part} {time_part}"

        datetime_obj = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M")
        return datetime_obj
                
    def parse_data(self, raw_data):
        soup = BeautifulSoup(raw_data, 'html.parser')
        all_data = soup.find_all('div', class_="tt_newsitem")

        result = []

        for data in all_data:
            if isinstance(data, Tag):
                tt_newstxt = data.find('div', class_='tt_newstxt media-body')
                title = tt_newstxt.find('h3').get_text(strip=True)
                url = tt_newstxt.find('a')['href']

                tt_figure = data.find('figure', class_='tt_figure pull-left')
                image_url = tt_figure.find('img')['src']

                date_str = tt_newstxt.find('span', class_='dates').get_text(strip=True)
                datetime_object = self.__extract_date_from_uz_date_str(date_str)

                if datetime_object:
                    result.append(
                        {
                            "title": title,
                            "url": "https://tuit.uz" + url,
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
