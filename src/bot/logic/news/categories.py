import random
import traceback
from datetime import datetime

from aiogram import Router, types, F, html, exceptions
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramBadRequest

from src.db.database import Database
from src.language.translator import LocalizedTranslator

from src.bot.structures.keyboards import common
from src.bot.structures.fsm.category import CategoryGroup


news_router = Router(name='news')


@news_router.message()
async def category_handler(message: types.Message, db: Database, state: FSMContext):
    text_and_emoji = message.text.split()
    category = text_and_emoji[0].lower()

    category = await db.category.get_by_name(category)

    if not category:
        return
    
    news = await db.news.get_all_by_category(category_id=category.id)
    images = [new.image_url for new in news]

    image_url = None
    for image in images:
        if image and 'darakchi.uz' not in image:
            image_url = image
            break

    contents = [
        f"{html.bold(value=new.title)}\n"
        f"{html.link(value=await db.source.get(new.source_id),link=new.url)}\t{new.formatted_date}\n\n" 
            for new in news
    ]

    result = "".join([content for content in contents[:4]])
    
    try:
        if image_url:
            await message.answer_photo(
                photo=image_url,
                caption = result,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=common.show_pagination_buttons()
            )
        else:
            await message.answer(
                text = result,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=common.show_pagination_buttons()
            )

        await state.set_state(CategoryGroup.step1)
        await state.update_data(
            contents = contents,
            images = images,
            start = 0,
            end = 4
        )
    except exceptions.TelegramBadRequest as tbr:
        print(tbr)


@news_router.callback_query(CategoryGroup.step1)
async def callback_pagination(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    images = data['images']
    contents = data['contents']
    start = data.get('start', 0)
    end = data.get('end', 4)

    try:
        if c.data == "next":
            if 0 < (len(contents) - end) < 4:
                start += 4
                end += (len(contents) - end)

            elif (len(contents) - end) > 0:
                start += 4
                end += 4
        
        elif c.data == "back":
            if start > 0:
                start, end = start-4, start
            
        result = "".join([content for content in contents[start:end]])
        image_url = None
        for image in images[start:end]:
            if image and 'darakchi.uz' not in image:
                image_url = image
                break

        if image_url:
            await c.message.edit_media(
                media=types.InputMediaPhoto(
                    media=image_url,
                    caption=result
                ),
                reply_markup=common.show_pagination_buttons(),
                disable_web_page_preview=True
            )
        elif not c.message.photo:
            await c.message.edit_text(
                text=result,
                reply_markup=common.show_pagination_buttons(),
                disable_web_page_preview=True
            )           
        else:
            await c.message.edit_caption(
                caption=result,
                reply_markup=common.show_pagination_buttons(),
            )
        await c.answer()

        await state.update_data(
            start=start,
            end=end
        )
    except TelegramBadRequest as tbr:
        print(tbr)
        await c.answer("No more data")
    
    except Exception as e:
        print(e)
