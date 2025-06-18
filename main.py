from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

# Замени на свой токен
BOT_TOKEN = "7572534113:AAFdRB_U0KSVK0rCTYlnPgd_Z2-Ij0WXZ0k"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    web_app_url = "https://fitness-webapp.vercel.app/index.html" 

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Рассчитать БЖУ", web_app={"url": "https://fitness-webapp.vercel.app/index.html"})],
        [InlineKeyboardButton(text="✉️ Личный вопрос", web_app={"url": "https://fitness-webapp.vercel.app/question.html"})] 
    ])

    await message.answer("Привет! Выберите, что вас интересует:", reply_markup=keyboard)

if __name__ == "__main__":
    dp.run_polling(bot)