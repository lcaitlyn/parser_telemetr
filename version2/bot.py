from lib2to3.pgen2 import token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

token = '5398322824:AAGdD38vs5_YRrHD5ZP0_abslEc0Ze1NyOk'

bot = Bot(token)
dp = Dispatcher(bot)


def on_startup():
    print('Бот запущен')


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_sticker(message.chat.id, open('stickers/pirate.tgs', 'rb'))
    markup = types.InlineKeyboardMarkup()
    mes = "Привет, <b>" + message.from_user.first_name + "</b>!\nЭто парсер телеметра 🏴‍☠️\n\n<b>Чтобы начать парсинг нажми кнопку внизу ⬇️</b>"
    await bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=markup)

@dp.message_handler()
async def echo_send(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup())