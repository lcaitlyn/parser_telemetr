import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='btn-light')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_html(url, params=None):
    r = requests.get(url, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='tr_even')

    channels = []
    for item in items:
        """
        if item.find('img'):
            print (item.find('img').get('src'))
        """
        if item.find('a', class_='kt-ch-title'):
            name = item.find('a', class_='kt-ch-title')
            channels.append({
                'title': name.get_text(),
                'link': name.get('href').replace('https://tmtr.me/', 'https://t.me/'),
                'photo': item.find('img').get('src'),
                'subscribers': item.find('span', attrs={'data-do': 'show_dynamic_participants'}).get_text(strip=True),
                'eyes': item.find('span', attrs={'data-do': 'show_dynamic_views'}).get_text(strip=True),
            })
    return channels


def print_channels(channels, bot, message):
    for channel in channels:
        mes = f'✏️ Название канала: <b>'
        + channel['title'] + '</b>\n🔗 Ссылка: <b>' + channel['link']
        + '</b>\n🙎‍♂️ Подписчиков: <b>' + channel['subscribers']
        + '</b>\n👀 Просмотров: <b>' + channel['eyes'] + '</b>'
        bot.send_photo(message.chat.id, channel['photo'], mes, parse_mode='html')
        

    

def parse(bot, message):
    URL = message.text
    html = get_html(URL)
    if html.status_code == 200:
        channels = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            bot.send_message(message.chat.id, '🔎 Парсинг страницы ' + str(page) + '/' + str(pages_count))
            html = get_html(URL, params={'page': page})
            channels.extend(get_content(html.text))
        print_channels(channels, bot, message)
        bot.send_message(message.chat.id, '📊 Парсинг успешно завершен.\nСпаршено <b>' + str(len(channels)) + '</b> каналов', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Ошибка: не удалось установить соединение с сайтом ❌')