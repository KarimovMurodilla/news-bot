import random
import traceback
from datetime import datetime

from aiogram import Router, types, F, html
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
    news = await db.news.get_all_by_category(category_id=category.id)

    contents = [
        f"{html.bold(value=new.title)}\n"
        f"{html.link(value=await db.source.get(new.source_id),link=new.url)}\t{new.formatted_date}\n\n" 
            for new in news
    ]

    result = "".join([content for content in contents[:5]])
    
    await message.answer(
        text = result,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=common.show_pagination_buttons()
    )

    await state.set_state(CategoryGroup.step1)
    await state.update_data(
        contents=contents,
        start = 0,
        end = 5
    )


@news_router.callback_query(CategoryGroup.step1)
async def callback_back(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    contents = data['contents']
    start = data.get('start', 0)
    end = data.get('end', 5)

    try:
        if c.data == "next":
            if 0 < (len(contents) - end) < 5:
                start += 5
                end += (len(contents) - end)

            elif (len(contents) - end) > 0:
                start += 5
                end += 5
        
        elif c.data == "back":
            if start > 0:
                start, end = start-5, start
            
        result = "".join([content for content in contents[start:end]])
        await c.message.edit_text(
            text=result,
            reply_markup=common.show_pagination_buttons(),
            disable_web_page_preview=True
        )
        await c.answer()
        
    except TelegramBadRequest:
        await c.answer("No more data")
    
    finally:
        await state.update_data(
            start=start,
            end=end
        )
