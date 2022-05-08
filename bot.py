from cgitb import html
from email import message
import telebot
from telebot import types
import parser
from parcer import parse


#URL = "https://telemetr.me/channels/?participants_to=10000"
t_url = 'https://telemetr.me/channels/'
token = 'your token from @botfather'
bot = telebot.TeleBot(token)
URL = ""

@bot.message_handler(commands=['start'])
def start(message):
    sticker = open ('stickers/pirate.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Начать парсинг', callback_data='start'))
    mes = "Привет, <b>" + message.from_user.first_name + "</b>!\nЭто парсер телеметра 🏴‍☠️\n\n<b>Чтобы начать парсинг нажми кнопку внизу ⬇️</b>"
    bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_message(message):
    bot.send_message(message.chat.id, message.text, parse_mode='html')

def get_url(message):
    if message.text.find(t_url, 0, len(t_url)) != -1:
        start_parse(message)
    else:
        bot.send_message(message.chat.id, "Неверная ссылка")
    

def start_parse(message):
    bot.register_next_step_handler(message, get_message)
    bot.send_message(message.chat.id, 'Парсинг начался...')
    parse(bot, message)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'start':
            bot.edit_message_text(text=call.message.text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None,)
            bot.send_message(call.message.chat.id, 'Введите ссылку. Пример: https://telemetr.me/channels/?participants_from=9999&participants_to=10000 \nhttps://telemetr.me/channels/?participants_to=10000')
            bot.register_next_step_handler(call.message, get_url)
        


bot.polling(none_stop=True, interval=0)

#parse()
