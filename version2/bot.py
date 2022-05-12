from lib2to3.pgen2 import token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

token = '5398322824:AAGdD38vs5_YRrHD5ZP0_abslEc0Ze1NyOk'

bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_send(message: types.Message):
    await bot.send_message(message.chat.id, message.text)



executor.start_polling(dp, skip_updates=True)