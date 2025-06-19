from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import F, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os

# === Подготовка ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# === FSM для вопросов ===
class QuestionState(StatesGroup):
    waiting_for_question = State()

# === Команда /start ===
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    web_app_url = "https://fitnessbo4a-webapp.vercel.app/index.html" 

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Рассчитать БЖУ", web_app={"url": web_app_url})],
        [InlineKeyboardButton(text="✉️ Личный вопрос", web_app={"url": "https://fitnessbo4a-webapp.vercel.app/question.html"})] 
    ])

    await message.answer("Привет! Выберите, что вас интересует:", reply_markup=keyboard)

# === Ответ администратора ===
@dp.message(F.from_user.id == ADMIN_ID, F.reply_to_message)
async def answer_to_user(message: Message):
    original = message.reply_to_message

    if not original or not original.text.startswith("📩 Вопрос от пользователя"):
        await message.answer("Вы можете отвечать только на вопросы от пользователей.")
        return

    try:
        user_id = int(original.text.split()[5])  # "Вопрос от пользователя 123456789..."
    except (IndexError, ValueError):
        await message.answer("Не удалось определить ID пользователя.")
        return

    try:
        await bot.send_message(user_id, f"💬 Ответ от эксперта:\n{message.text}")
        await message.answer(f"✅ Ответ отправлен пользователю {user_id}.")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить ответ: {e}")

# === Если ты хочешь тестировать локально — запуск бота ===
if __name__ == "__main__":
    dp.run_polling(bot)