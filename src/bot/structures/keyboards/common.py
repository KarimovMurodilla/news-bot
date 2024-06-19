from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from src.language.translator import LocalizedTranslator


def show_languages():
    kb = [
        [types.KeyboardButton(text="🇺🇿 O'zbek")],
        [types.KeyboardButton(text="🇷🇺 Русский")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def show_categories():
    kb = [
        [
            types.KeyboardButton(text="Jamiyat 👫🏻"),
            types.KeyboardButton(text="Sport 🥇")
        ],
        [
            types.KeyboardButton(text="Siyosat 📝"),
            types.KeyboardButton(text="Iqtisodiyot 💵")
        ],
        [
            types.KeyboardButton(text="Texnologiya 🤖"),
            types.KeyboardButton(text="Dunyo 🌍")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def show_categories_inline():
    kb = [
        [types.InlineKeyboardButton(text="Jamiyat", callback_data='jamiyat')],
        [types.InlineKeyboardButton(text="Sport", callback_data='sport')],
        [types.InlineKeyboardButton(text="Siyosat", callback_data='siyosat')],
        [types.InlineKeyboardButton(text="Iqtisodiyot", callback_data='iqtisodiyot')],
        [types.InlineKeyboardButton(text="Texnologiya", callback_data='texnologiya')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True)

    return keyboard


def show_pagination_buttons():
    kb = [
        [
            types.InlineKeyboardButton(text="⬅️", callback_data='back'),
            types.InlineKeyboardButton(text="➡️", callback_data='next'),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard
