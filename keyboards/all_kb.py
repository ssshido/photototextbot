from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins

def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📖 Рукописный текст"), KeyboardButton(text="📖 Печатный текст")],
        [KeyboardButton(text="📝 Перевести текст"), KeyboardButton(text="🔢 Решить математический пример")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard