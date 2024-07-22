import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import Router
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import F

import requests
import asyncio

API_TOKEN = '7491361835:AAFcjeMHdHIAAEfC6ckrx6qKQZeXWveAvYI'
LARAVEL_API_URL = 'https://5553388d3eb8b32d.mokky.dev'
ADMIN_ID = 5580150613

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Настройка роутера
router = Router()
dp.include_router(router)

# Обработчик команды /support
@router.message(Command('support'))
async def handle_support(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_name = message.chat.title
    text = message.text.replace('/support', '').strip().replace('\n', ' ')

    if text:
        data = {
            'user_id': user_id,
            'text': text,
            'group_id': chat_id,
            'group_name': chat_name
        }
        response = requests.post(f'{LARAVEL_API_URL}/tasks', json=data)

        if response.status_code == 201:
            await message.reply("Ваше сообщение сохранено. Ждите ответ.")
        else:
            await message.reply("Произошла ошибка при сохранении сообщения.")
    else:
        await message.reply("Пожалуйста, отправьте сообщение в формате /support Ваше сообщение")

# Функция для отправки сообщений в группы от администратора
@router.message(Command('message'))
async def message_to_groups(message: types.Message):
    user_id = message.from_user.id

    if user_id == ADMIN_ID:
        text = message.text.replace('/message', '').strip().replace('\n', ' ')

        if text:
            data = {
                'user_id': user_id,
                'text': text
            }
            response = requests.post(f'{LARAVEL_API_URL}/message_to_groups', json=data)

            if response.status_code == 201:
                await message.reply("Ваше сообщение отправлено.")
            else:
                await message.reply("Произошла ошибка при отправке сообщения.")
        else:
            await message.reply("Пожалуйста, отправьте сообщение в формате /message Ваше сообщение")
    else:
        await message.reply("У вас нет прав для отправки сообщений в группы.")

async def on_startup():
    await bot.set_my_commands([
        BotCommand(command="/support", description="Отправить сообщение в поддержку"),
        BotCommand(command="/message", description="Отправить сообщение в группы")
    ])

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
