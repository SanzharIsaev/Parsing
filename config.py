import telebot
from telebot import types
from config import *
import requests

API = "a47f5a507150f1710b930ed668b98c75"
bot = telebot.TeleBot('6955901262:AAGD2ne4kSgz-fjkL78LUp8anyl_eYvtayw')
markup = types.ReplyKeyboardMarkup(True, False)
markup.row('Поиск', 'Команды')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Поиск', 'Команды')
    bot.send_message(message.chat.id, "Привет {}. Выбери команду ".format(message.from_user.username,
                                                                          bot.get_me()), parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(commands=["город"])
def heandle_stop(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Бишкек')
    item2 = types.KeyboardButton('Москва')
    item3 = types.KeyboardButton('Алматы')
    item4 = types.KeyboardButton('Ташкент')
    item5 = types.KeyboardButton('Рим')
    item6 = types.KeyboardButton('/назад')
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, "Выбери город где хочешь узнать прогноз погоды", reply_markup=markup)


@bot.message_handler(commands=['Дата'])
def apple_collections(message):
    markup = types.ReplyKeyboardMarkup(True, False)
    markup.row("Текущий прогноз погоды")
    markup.row("Прогноз на неделю")
    markup.row("/back")
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


@bot.message_handler(commands=["стоп"])
def heandle_stop(message):
    remove_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Заглядывай чаще!", reply_markup=remove_markup)


@bot.message_handler(commands=["помощь"])
def heandle_help(message):
    bot.send_message(message.chat.id, """Мои возможности весьма спецефичны, но, ты тоько псомотри!
    Всё работает!!!""")


@bot.message_handler(commands=['назад'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Поиск', 'Команды')
    bot.send_message(message.chat.id, "Выбери команду ".format(message.from_user.username,
                                                               bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def heandle_text(message):
    if message.text == 'Команды':
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.row('/старт', '/город', '/дата', '/помощь', '/стоп', '/назад')
        bot.send_message(message.chat.id, """Выбери команду: """, reply_markup=markup)
    elif message.text == 'Поиск':
        msg = f'<b>Укажите город:</b>'
        bot.send_message(message.chat.id, msg, parse_mode="html")
    else:
        try:
            a = open('weather.txt', 'w')
            CITY = message.text
            URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API}'
            data = requests.get(url=URL)
            print(data.text)
            a.write(data.text)
            response = requests.get(url=URL).json()
            city_info = {
                "city": CITY,
                'temp': response['main']['temp'],
                'weather': response['weather'][0]['description'],
                'wind': response['wind']['speed'],
                'pressure': response['main']['pressure'],
            }
            msg = f"<b><u>{CITY.upper()}</u></b>\n\n<b>Weather: {city_info['weather']}</b>\n----------------------------------\nTemperature: <b>{city_info['temp']} C</b>\n----------------------------------\nWind: <b>{city_info['wind']} m/s</b>\n----------------------------------\nPressure: <b>{city_info['pressure']}hPa</b>"
            bot.send_message(message.chat.id, msg, parse_mode="html")
        except:
            msg1 = f"<b> Nothing found to country. Try again</b>"
            bot.send_message(message.chat.id, msg1, parse_mode="html")


bot.polling(non_stop=True)
