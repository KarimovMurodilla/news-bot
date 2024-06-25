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


class XabarUzParser(BaseParser):
    name = "xabar.uz"

    def _load_attrs(self, category, url, language):
        self.category = category
        self.url = url
        self.language = language

    async def fetch_data(self):
        url = self.url
        url = 'https://xabar.uz/uz/siyosat'

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
        now = datetime.now()

        if 'bugun' in date_str:
            date_part = now.date()  # Today's date
            time_part = date_str.split('.')[0].strip()[-5:]
            datetime_str = f"{date_part} {time_part}"
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

            return datetime_obj
                
    def parse_data(self, raw_data):
        soup = BeautifulSoup(raw_data, 'html.parser')
        all_data = soup.find('div', class_=['latest__news-list'])

        result = []

        print("Len of data:", raw_data)

        for data in all_data:
            if isinstance(data, Tag):
                news_title = data.find('p', class_='news__item-title')
                title = news_title.get_text()
                url = news_title.find('a')['href']

                news_meta = data.find('p', class_='news__item-meta')
                date_str = news_meta.get_text()

                datetime_object = self.__extract_date_from_uz_date_str(date_str)

                # if datetime_object:
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

        print(result)
        # return result

    async def save_data(self, parsed_data):
        async with AsyncSession(self.engine) as session:
            db = Database(session)
            data_store = DataStorage()
            await data_store.save_to_db(db, parsed_data)
