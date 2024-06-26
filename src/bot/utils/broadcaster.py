import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Bot, exceptions, html
from aiogram.client.default import DefaultBotProperties

from src.db.database import Database
from src.configuration import conf
from src.db.database import create_async_engine


class Broadcaster:
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

            news = await db.news.get_recent_news_last_5_minutes()

            result_d = {}

            category_with_emoji = {
                "jamiyat": "#jamiyat 👫🏻",
                "sport": "#sport 🥇",
                "siyosat": "#siyosat 📝",
                "iqtisodiyot": "#iqtisodiyot 💵",
                "texnologiya": "#texnologiya 🤖",
                "dunyo": "#dunyo 🌍"
            }

            print("Len of news:", len(news))
            # if len(news) < 3:
            #     return

            # content = [
            #     f"- {html.bold(value=new.title)}\n" \
            #     f"{html.link(value=await db.source.get(new.source_id),link=new.url)}\t{new.formatted_date}\n\n"
            #     for new in news[:3]
            # ]

            result = []
            count = 0
            for new in news:
                count += 1
                category = await db.category.get(new.category_id)
                category_name = category_with_emoji[category.name]

                content =   f"- {html.bold(value=new.title)}\n" \
                            f"{html.link(value=await db.source.get(new.source_id),link=new.url)}\t{new.formatted_date}\n\n"
                
                if not result_d.get(category_name):
                    result_d[category_name] = []

                # if len(result_d.get(category_name)) < 3:
                result_d[category_name].append(content)

                if count >= 3:
                    break

            result = [f"{i[0]}\n{''.join(i[1])}" for i in result_d.items()]
            # result = "".join(content)
            if not result:
                return
            
            final_text = "".join(result) + "👉 @uzvip_news"

            image_url = None
            for new in news:
                if new.image_url and 'darakchi.uz' not in new.image_url:
                    image_url = new.image_url
                    break

            return final_text, image_url

    async def send_message(self, user_id: int, message: str, disable_notification: bool = False) -> bool:
        """
        Safe messages sender

        :param user_id:
        :param text:
        :param disable_notification:
        :return:
        """
        try:
            if message[1]:
                await self.bot.send_photo(
                    chat_id=user_id,
                    photo=message[1],
                    caption=message[0],
                    disable_notification=disable_notification
                )
            else:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message[0],
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
            return await self.send_message(user_id, message)  # Recursive call
        except exceptions.TelegramBadRequest as tbr:
            print(tbr)
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

            if not message:
                return
            
            # for user_id in users:
            await self.send_message(conf.CHANNEL_ID, message)
            #     count += 1
            # await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
        finally:
            self.log.info(f"{count} messages successful sent.")

        return count
