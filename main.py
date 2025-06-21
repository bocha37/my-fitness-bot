from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

# Токен бота
BOT_TOKEN = "7572534113:AAFdRB_U0KSVK0rCTYlnPgd_Z2-Ij0WXZ0k"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Рассчитать БЖУ", web_app={"url": "https://fitnessbo4a-webapp.vercel.app"})], 
        [InlineKeyboardButton(text="✉️ Личный вопрос", web_app={"url": "https://fitnessbo4a-webapp.vercel.app/question.html"})], 
        [InlineKeyboardButton(text="❤️ Здоровье", web_app={"url": "https://fitnessbo4a-webapp.vercel.app/health.html"})] 
    ])
    await message.answer("Привет! Выберите, что вас интересует:", reply_markup=keyboard)

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)