import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"🏔️ Привет, {name}! Я — NomadConnect. Рад тебя видеть!")

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("📋 Доступные команды:\n/start — Приветствие\n/help — Помощь")

@dp.message()
async def any_message(message: types.Message):
    await message.answer("Я пока учусь. Напиши /help, чтобы узнать команды.")

async def health_check(request):
    return web.Response(text="Бот работает!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    print("🌐 Веб-сервер запущен на порту 10000")

async def main():
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())

