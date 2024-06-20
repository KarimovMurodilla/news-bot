import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Bot, exceptions, html
from aiogram.client.default import DefaultBotProperties

from src.db.database import Database
from src.configuration import conf
from src.db.database import create_async_engine


class Broadcast:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('broadcast')
        self.engine = create_async_engine(url=conf.db.build_connection_str())

        self.bot = Bot(token=conf.bot.token, default=DefaultBotProperties(parse_mode='html'))
        
    async def get_users(self):
        async with AsyncSession(self.engine) as session:
            db = Database(session)

            result = await db.user.get_all_users()
            users = [user.user_id for user in result]
            return users
        
    async def get_message(self):
        async with AsyncSession(self.engine) as session:
            db = Database(session)

            news = await db.news.get_recent_news_last_15_minutes()

            result_d = {}

            category_with_emoji = {
                "jamiyat": "Jamiyat 👫🏻",
                "sport": "Sport 🥇",
                "siyosat": "Siyosat 📝",
                "iqtisodiyot": "Iqtisodiyot 💵",
                "texnologiya": "Texnologiya 🤖",
                "dunyo": "Dunyo 🌍"
            }

            for new in news:
                category = await db.category.get(new.category_id)
                category_name = category_with_emoji[category.name]

                content =   f"- {html.bold(value=new.title)}\n" \
                            f"{html.link(value=await db.source.get(new.source_id),link=new.url)}\t{new.formatted_date}\n\n"
                
                if not result_d.get(category_name):
                    result_d[category_name] = []

                if len(result_d.get(category_name)) < 3:
                    result_d[category_name].append(content)

            result = [f"{i[0]}\n\n{''.join(i[1])}" for i in result_d.items()]
            final_text = "Oxirgi yangiliklar:\n\n" + "".join(result)

            return final_text

    async def send_message(self, user_id: int, text: str, disable_notification: bool = False) -> bool:
        """
        Safe messages sender

        :param user_id:
        :param text:
        :param disable_notification:
        :return:
        """
        try:
            await self.bot.send_message(
                chat_id=user_id, 
                text=text, 
                disable_notification=disable_notification,
                disable_web_page_preview=True
            )
        except exceptions.TelegramForbiddenError:
            self.log.error(f"Target [ID:{user_id}]: blocked by user")
            async with AsyncSession(self.engine) as session:
                db = Database(session)
                await db.user.update_user(user_id, is_active=False)
        except exceptions.TelegramNotFound:
            self.log.error(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.TelegramRetryAfter as e:
            self.log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
            await asyncio.sleep(e.retry_after)
            return await self.send_message(user_id, text)  # Recursive call
        except exceptions.TelegramBadRequest:
            self.log.error(f"Target [ID:{user_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            self.log.exception(f"Target [ID:{user_id}]: failed")
        else:
            self.log.info(f"Target [ID:{user_id}]: success")
            return True
        finally:
            await self.bot.session.close()
        return False

    async def broadcast(self) -> int:
        """
        Simple broadcaster

        :return: Count of messages
        """
        count = 0
        try:
            users = await self.get_users()
            message = await self.get_message()
            for user_id in users:
                if await self.send_message(user_id, message):
                    count += 1
                await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
        finally:
            self.log.info(f"{count} messages successful sent.")

        return count
