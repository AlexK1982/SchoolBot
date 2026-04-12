import asyncio
import os
from time_utils import now_local

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from service import (
    load_schedule,
    get_schedule_for_day,
    format_day_schedule,
    get_current_slot,
    format_current_slot,
    get_next_lesson,
    format_next_lesson,
)
from nlp import detect_intent, extract_weekday, extract_class_name
from storage import set_user_class, get_user_class, init_db


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден")

schedule = load_schedule()

bot = Bot(token=TOKEN)
dp = Dispatcher()
init_db()

def get_today_weekday():
    return now_local().strftime("%A").lower()

def get_help_text() -> str:
    return (
        "Привет! Я бот с расписанием.\n\n"
        "Сначала выбери класс:\n"
        "/setclass 3Б\n\n"
        "Полезные команды:\n"
        "/help — показать подсказку\n"
        "/setclass 3Б — сохранить класс\n"
        "/myclass — показать сохраненный класс\n\n"
        "Можно писать так:\n"
        "• что сегодня\n"
        "• что завтра\n"
        "• что сейчас\n"
        "• что дальше\n"
        "• что у 3Б в понедельник"
    )

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(get_help_text(), reply_markup=get_main_keyboard())

@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(get_help_text(), reply_markup=get_main_keyboard())

@dp.message(Command("setclass"))
async def set_class_handler(message: Message):
    user_text = message.text or ""
    class_name = extract_class_name(user_text)

    if not class_name:
        await message.answer("Не понял класс.\nПример: /setclass 3Б")
        return

    set_user_class(message.from_user.id, class_name)
    await message.answer(f"Готово ✅\nЗапомнил твой класс: {class_name}")


@dp.message(Command("myclass"))
async def my_class_handler(message: Message):
    class_name = get_user_class(message.from_user.id)

    if not class_name:
        await message.answer("Класс пока не сохранен.\nИспользуй: /setclass 3Б")
        return

    await message.answer(f"Твой сохраненный класс: {class_name}")


@dp.message()
async def message_handler(message: Message):
    user_text = message.text or ""

    # обработка кнопок
    if user_text == "📅 Сегодня":
        user_text = "что сегодня"

    elif user_text == "📆 Завтра":
        user_text = "что завтра"

    elif user_text == "⏰ Сейчас":
        user_text = "что сейчас"

    elif user_text == "➡️ Следующий":
        user_text = "что дальше"
    intent = detect_intent(user_text)
    weekday = extract_weekday(user_text)
    class_name = extract_class_name(user_text)

    if not class_name:
        class_name = get_user_class(message.from_user.id)

    if not class_name:
        await message.answer(
            "Не понял запрос 🤔\n\n"
            "Попробуй так:\n"
            "• что сегодня\n"
            "• что завтра\n"
            "• что сейчас\n"
            "• что дальше\n"
            "• /setclass 3Б\n"
            "• /help"
        )
        return

    if not weekday:
        weekday = get_today_weekday()

    if intent == "day":
        lessons = get_schedule_for_day(schedule, weekday)
        response = format_day_schedule(class_name, weekday, lessons)
        await message.answer(response)
        return

    if intent == "current":
        current_time = now_local().strftime("%H:%M")
        current_slot = get_current_slot(schedule, weekday, current_time)
        response = format_current_slot(class_name, weekday, current_slot)
        await message.answer(response)
        return

    if intent == "next":
        current_time = now_local().strftime("%H:%M")
        next_lesson = get_next_lesson(schedule, weekday, current_time)
        response = format_next_lesson(class_name, weekday, next_lesson)
        await message.answer(response)
        return

    await message.answer(
        "Не понял запрос 🤔\n\n"
        "Попробуй так:\n"
        "• что сегодня\n"
        "• что завтра\n"
        "• что сейчас\n"
        "• что дальше\n"
        "• /setclass 3Б"
    )
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Сегодня"), KeyboardButton(text="📆 Завтра")],
            [KeyboardButton(text="⏰ Сейчас"), KeyboardButton(text="➡️ Следующий")],
        ],
        resize_keyboard=True
    )
    return keyboard

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())