from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def start(user_id):
    web_app_url = f"https://testedsite.ru/users/login/{user_id}/"  # URL of your web application
    web_app_button = InlineKeyboardButton(text="Play🎮", web_app=WebAppInfo(url=web_app_url))
    community = InlineKeyboardButton(text="Community 😎", url="https://t.me/vape_comunnity")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button], [community]])
    return keyboard

