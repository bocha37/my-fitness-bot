from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web
import asyncio

# Токен бота
BOT_TOKEN = "7572534113:AAFdRB_U0KSVK0rCTYlnPgd_Z2-Ij0WXZ0k"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранение вопросов (можно потом сохранять в БД)
questions = []

# === API маршрут для получения данных с WebApp ===
async def receive_question(request):
    try:
        data = await request.json()
        question_text = data.get("question")
        user_id = data.get("user_id")

        if question_text and user_id:
            questions.append({"user_id": user_id, "question": question_text})
            print(f"Получен вопрос от {user_id}: {question_text}")
            return web.json_response({"status": "ok"})
        else:
            return web.json_response({"status": "error", "message": "Invalid data"}, status=400)
    except Exception as e:
        print("Ошибка:", e)
        return web.json_response({"status": "error", "message": "Server error"}, status=500)

# === Команда /start ===
@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Рассчитать БЖУ", web_app={"url": "https://fitnessbo4a-webapp.vercel.app"})], 
        [InlineKeyboardButton(text="✉️ Личный вопрос", web_app={"url": "https://fitnessbo4a-webapp.vercel.app/question.html"})] 
    ])
    await message.answer("Привет! Выберите, что вас интересует:", reply_markup=keyboard)

# === Запуск бота + веб-сервера ===
async def start_bot_and_server():
    app = web.Application()
    app.router.add_post('/question', receive_question)  # Маршрут для получения вопросов

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=8080)
    await site.start()

    print("Бот и сервер запущены...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot_and_server())