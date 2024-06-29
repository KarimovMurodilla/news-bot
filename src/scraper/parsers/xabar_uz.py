import asyncio
import aiohttp

from aiohttp import ClientSession, ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta
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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        try:
            async with ClientSession(trust_env=True, headers=headers) as session:
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
        now = datetime.now()

        if 'bugun' in date_str:
            date_part = now.date()  # Today's date
            time_part = date_str.split('.')[0].strip()[-5:]
            datetime_str = f"{date_part} {time_part}"
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        elif 'soat' in date_str:
            hour = date_str.split()[0]
            datetime_obj = now - timedelta(hours=int(hour))
            datetime_obj = datetime_obj.replace(microsecond=0)

        elif 'daqiqa' in date_str:
            minute = date_str.split()[0]
            datetime_obj = now - timedelta(minutes=int(minute))
            datetime_obj = datetime_obj.replace(microsecond=0)
        
        else:
            return

        return datetime_obj
                
    def parse_data(self, raw_data):
        soup = BeautifulSoup(raw_data, 'html.parser')
        all_data = soup.find('div', class_=['latest__news-list'])

        result = []

        for data in all_data:
            if isinstance(data, Tag):
                news_title = data.find('p', class_='news__item-title')
                title = news_title.get_text(strip=True)
                url = news_title.find('a')['href']

                news_meta = data.find('p', class_='news__item-meta')
                if not news_meta:
                    news_meta = data.find('div', class_='news__item-meta') 
                    date_time = news_meta.find('span', class_='date-time') 
                    date_str = date_time.get_text(strip=True)
                else:
                    date_str = news_meta.get_text(strip=True)

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
