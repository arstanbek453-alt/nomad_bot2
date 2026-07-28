import asyncio
from aiogram import Bot, Dispatcher, types
from datetime import datetime
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def main_menu():
    buttons = [
        [KeyboardButton(text="📅 Расписание")],
        [KeyboardButton(text="📍 Локации")],
        [KeyboardButton(text="💬 Оставить мнение")],
        [KeyboardButton(text="✨ Комплимент")],
        [KeyboardButton(text="❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


@dp.message(Command("start"))
async def start_command(message: types.Message):
    name = message.from_user.first_name

    text = (
        f"🏔️ *Салам, {name}!* Добро пожаловать в мир кочевников.\n\n"
        "Я — твой спутник на Всемирных играх кочевников 2026.\n"
        "Помогаю находить жильё, события, людей и впечатления.\n\n"
        "🌾 Наш бот — это мост между гостями и хозяевами, между мирами и судьбами.\n\n"
        "👇 Нажми на кнопку, чтобы начать."
    )

    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu())


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("📋 Доступные команды:\n/start — Приветствие\n/help — Помощь")


@dp.message(Command("time"))
async def time_command(message: types.Message):
    now = datetime.now().strftime("%H:%M:%S")
    await message.answer(f"🕐 Сейчас {now}")

@dp.message(Command("schedule"))
async def schedule_command(message: types.Message):
    text = (
        "📅 *Расписание Игр кочевников 2026*\n\n"
        "🏔️ 31 августа — Открытие в Бишкеке\n"
        "🚌 1 сентября — Переезд на Иссык-Куль\n"
        "🏹 2–6 сентября — Основные соревнования\n"
        "🎭 6 сентября — Закрытие в Чолпон-Ате\n\n"
        "Подробное расписание будет добавляться по мере уточнения."
    )
    await message.answer(text, parse_mode="Markdown")


# Список комплиментов
compliments = [
    "Ты сегодня невероятно продуктивен! 💪",
    "У тебя отличный вкус! 🌟",
    "Ты делаешь этот мир лучше! 🌍",
    "Твой код сегодня особенно красив! 💻",
    "Ты — настоящий Архитектор! 🏔️"
]

@dp.message(Command("compliment"))
async def compliment_command(message: types.Message):
    comp = random.choice(compliments)
    await message.answer(f"✨ {comp}")

@dp.message(Command("places"))
async def places_command(message: types.Message):
    text = (
        "📍 *Главные локации Игр кочевников 2026*\n\n"
        "🏔️ *Кырчын* — этногородок, главная площадка\n"
        "🏟️ *Бишкек-Арена* — открытие 31 августа\n"
        "🏞️ *Чолпон-Ата* — соревнования и закрытие\n"
        "🎶 *Рух-Ордо* — культурная программа\n\n"
        "Подробнее о каждой локации — в следующих обновлениях."
    )
    await message.answer(text, parse_mode="Markdown")

# Временное хранилище: кто сейчас в режиме "оставления отзыва"
waiting_for_feedback = set()

@dp.message(Command("feedback"))
async def feedback_start(message: types.Message):
    waiting_for_feedback.add(message.from_user.id)
    await message.answer(
        "💬 *Оставь своё мнение об Играх кочевников!*\n\n"
        "Напиши всё, что хочешь сказать. Анонимно.\n"
        "Твой голос будет передан организаторам 🌾\n\n"
        "(Просто напиши сообщение — и оно будет сохранено)"
    )
@dp.message(lambda message: message.text == "📅 Расписание")
async def schedule_button(message: types.Message):
    await schedule_command(message)

@dp.message(lambda message: message.text == "📍 Локации")
async def places_button(message: types.Message):
    await places_command(message)

@dp.message(lambda message: message.text == "💬 Оставить мнение")
async def feedback_button(message: types.Message):
    await feedback_start(message)

@dp.message(lambda message: message.text == "✨ Комплимент")
async def compliment_button(message: types.Message):
    await compliment_command(message)

@dp.message(lambda message: message.text == "❓ Помощь")
async def help_button(message: types.Message):
    await help_command(message)


@dp.message()
async def save_feedback(message: types.Message):
    user_id = message.from_user.id

    # Если пользователь в режиме "отзыва"
    if user_id in waiting_for_feedback:
        waiting_for_feedback.remove(user_id)
        feedback_text = message.text

        # Сохраняем в файл
        with open("feedback.txt", "a", encoding="utf-8") as f:
            f.write(f"{feedback_text}\n")

        await message.answer("🌾 Спасибо! Твоё мнение передано.")
        return

    # Если это обычное сообщение (не команда)
    await message.answer("Я пока учусь. Напиши /help, чтобы узнать команды.")


@dp.message()
async def any_message(message: types.Message):
    await message.answer("Я пока учусь. Напиши /help, чтобы узнать команды.")


async def main():
    print("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
