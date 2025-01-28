import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.utils.markdown import hide_link


import database
from translations import LANGUAGES, DEFAULT_LANGUAGE
from tools import get_preferred_language

API_TOKEN = 'token'

logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# ------------------------------------------------------------------------------------------------------

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    user_lang = get_preferred_language(message.from_user.id, message.from_user.language_code)
    await message.answer(LANGUAGES[user_lang]['welcome'])

# Хэндлер на команду /set_token
@dp.message(Command("set_token"))
async def cmd_send_token(message: types.Message):
    user_lang = get_preferred_language(message.from_user.id, message.from_user.language_code)
    await message.answer(LANGUAGES[user_lang]['send_token'])

# ------------------------------------------------------------------------------------------------------
                #    оплата подписки

@dp.callback_query_handler(lambda c: c.data == 'pay_for_subscription')
async def process_payment(callback_query: types.CallbackQuery):
    # Логика обработки оплаты (например, интеграция с платежным шлюзом)
    if payment_successful:
        await bot.send_message(callback_query.from_user.id, "Подписка оплачена! Пожалуйста, отправьте токен вашего бота.")

# ------------------------------------------------------------------------------------------------------

                #  получение токена и активация функционала

@dp.message_handler(lambda message: message.text.startswith('TOKEN:'))
async def activate_user_bot(message: types.Message):
    user_token = message.text.split(':')[1].strip()
    user_bot = Bot(token=user_token)

    # Сохраните этот токен в базе данных, чтобы знать, что у этого пользователя есть активная подписка
    database.save_user_subscription(message.from_user.id, user_token)

    # Здесь вы можете, например, отправить приветственное сообщение в боте пользователя
    await user_bot.send_message(message.from_user.id, "Ваш бот активирован для приема отзывов и предложений!")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
