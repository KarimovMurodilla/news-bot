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


class YuzUzParser(BaseParser):
    name = "yuz.uz"

    def _load_attrs(self, category, url, language):
        self.category = category
        self.url = url
        self.language = language

    def __extract_date_from_uz_date_str(self, date_str: str):
        uzbek_months = {
            "Yanvar": "01",
            "Fevral": "02",
            "Mart": "03",
            "Aprel": "04",
            "May": "05",
            "Iyun": "06",
            "Iyul": "07",
            "Avgust": "08",
            "Sentyabr": "09",
            "Oktyabr": "10",
            "Noyabr": "11",
            "Dekabr": "12"
        }

        day, month_time = date_str.split(" ", 1)
        month_name, time = month_time.split(", ")
        month_num = uzbek_months[month_name]
        formatted_date_str = f"{day}.{month_num}.2024, {time}"
        format_str = "%d.%m.%Y, %H:%M"
        date_obj = datetime.strptime(formatted_date_str, format_str)

        return date_obj

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
        all_data = soup.find('div', class_=['pages-content__main'])

        result = []

        for data in all_data:
            if isinstance(data, Tag):
                item_content = data.find('div', class_="newsItem-content")
                a_tag = item_content.find('a')
                url = a_tag['href']
                title = a_tag.find('h2', class_="newsItem-title").get_text(strip=True)

                item_data = data.find('div', class_="newsItem-data")
                item_month = item_data.find('span', class_="newsItem-month").get_text()
                item_time = item_data.find('span', class_="newsItem-time").get_text(strip=True)
                date_str = f"{item_month}, {item_time}"
                datetime_object = self.__extract_date_from_uz_date_str(date_str)

                item_image = data.find('div', class_="newsItem-image")
                image_tag = item_image.find('img', class_="slider__image")['data-srcset']
                image_url = image_tag.strip().split(',')[-2].split()[0]

                result.append(
                    {
                        "title": title,
                        "url": f"https://{self.name}{url}",
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
