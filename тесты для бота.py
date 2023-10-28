#блок 1
from telebot import *

import requests
from requests import get


from pyowm import OWM


import sqlite3


from pycbrf.toolbox import ExchangeRates

from datetime import date


owm = OWM('33cf41809d5489af95160f6aa02859d7')
mgr = owm.weather_manager()


deadlines ={}

#блок 2
def adek(s):    #функция привода вводимого текста в нижний регистр
    return s.lower()

#вспомогательные переменнные
hello_text = 'Привет! Я помогу немного упростить дела ⭐️'
main_menu_text = 'Выбери, что хочешь посмотреть'
mistake_text = 'Не совсем понимаю, что ты имеешь в виду.'

task = ''

#вводим самого бота
bot = telebot.TeleBot('6905070702:AAH3zTaXXhJwodcHMjTdrT5F5iLZn3l7EKk')


#блок 3
@bot.message_handler(commands=['help'])
def user(help):
    bot.send_message(help.chat.id, mistake_text)

@bot.message_handler(commands=['start'])
def user(message):
    st = adek(message.text)
    knop = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
    knop.add(telebot.types.KeyboardButton('Начнем!'))

    bot.send_message(message.chat.id, hello_text, reply_markup=knop)

    bot.send_photo(message.chat.id, get('https://i.pinimg.com/564x/59/f9/b2/59f9b2507ccd8bfcfd40a32f39a57373.jpg').content)

    bot.register_next_step_handler(message, menu)



#блок 4
@bot.message_handler(commands=['text'])
def menu(message):
    st = adek(message.text)
    if st == 'начнем!' or st == 'главное меню':
        knop = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton('погода ⛅️')
        but2 = types.KeyboardButton('валюты 💸')
        but3 = types.KeyboardButton('дедлайны 🚩')
        but4 = types.KeyboardButton('помощь 🆘')
        knop.add(but1, but2, but3, but4)
        bot.send_message(message.chat.id, main_menu_text, reply_markup=knop)
        bot.register_next_step_handler(message, choose)

    elif st == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)

    else:
        bot.send_message(message.chat.id, mistake_text)
        user(message)




@bot.message_handler()
#блок 5
def choose(message):
    st = adek(message.text)
    if st == 'погода ⛅️':
        pogoda(message)
    elif st =='валюты 💸':
        summa(message)
    elif st == 'помощь 🆘':
        help(message)
    elif st == 'дедлайны 🚩':
        dead(message)
    elif st == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)
    else:
        bot.send_message(message.from_user.id, 'Произошла ошибка. Попробуй снова')
        user(message)
@bot.message_handler()
#блок 6
def pogoda(message):
    bot.send_photo(message.chat.id, get('https://i.pinimg.com/564x/0e/91/4d/0e914de3125362a619b969be10b291a7.jpg').content)
    bot.send_message(message.from_user.id, 'Погода в каком городе требуется?')
    bot.register_next_step_handler(message, get_weathers)

@bot.message_handler()
def get_weathers(message):
    city = adek(message.text)
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=33cf41809d5489af95160f6aa02859d7'

    try:
        if adek(message.text) == '/start':
            bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
            user(message)
        else:
            weather_data = requests.get(url).json()
            temperature = round(weather_data['main']['temp'])
            temperature_feels = round(weather_data['main']['feels_like'])

            information = '⭐️ В данный момент в городе ' + city.title() + ': ' + str(temperature) + '°C' '\n'
            information += '⭐️ По ощущениям'  ': ' + str(temperature_feels) + '°C' '\n'
            information += '' '\n'

            if temperature_feels <= -10:
                information += '❗️Очень холодно. Лучше не выходить из дома без необходимости.'
            elif -10 < temperature_feels < 0:
                information += '❗Холодно. Не забудь одеться теплее.'
            elif 0 <= temperature_feels < 10:
                information += '❗Температура стремится к нулю.'
            elif 10 <= temperature_feels <= 20:
                information += '❗Прохладно, но при этом комфортно.'
            elif 20 < temperature_feels < 30:
                information += '❗Отличная погода для прогулки.'
            elif temperature_feels >= 30:
                information += '❗Очень жарко. Не забывай соблюдать водный баланс!'
    except Exception:
        information = '❗❗Город не найден, повторите запрос! ❗❗'

    bot.send_message(message.chat.id, information)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = (telebot.types.KeyboardButton('сменить город'))
    btn2 = (telebot.types.KeyboardButton('главное меню'))

    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    bot.register_next_step_handler(message, next_step)

def next_step(message):
    choice = adek(message.text)
    if choice == 'сменить город':
        pogoda(message)

    elif choice == 'главное меню':
        quit(message)

    elif choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)

    else:
        bot.send_message(message.chat.id, '❗❗Город не найден, повторите запрос! ❗❗')
        pogoda(message)

def quit(message):
    menu(message)

#блок 7
@bot.message_handler()
def summa(message):
    bot.send_photo(message.chat.id, get('https://i.pinimg.com/564x/91/d0/56/91d05626656a100f22c9fb3fdfa4ae34.jpg').content)
    bot.send_message(message.from_user.id, 'Введите сумму (целым числом) в той валюте, которую хотите перевести 🤑')
    bot.register_next_step_handler(message, summa_next)


def summa_next(message):
    global amount
    choice = adek(message.text)

    if choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)
    try:
        amount = int(message.text)
        if amount > 0:
            markup = types.ReplyKeyboardMarkup(row_width=3)
            but1 = types.InlineKeyboardButton('доллар')
            but2 = types.InlineKeyboardButton('евро')
            but3 = types.InlineKeyboardButton('юань ')
            but4 = types.InlineKeyboardButton('фунт')
            but5 = types.InlineKeyboardButton('главное меню')

            markup.add(but1, but2, but3, but4, but5)
            bot.send_message(message.chat.id, 'Выберите валюту!', reply_markup=markup)
            bot.register_next_step_handler(message, step_on)


        else:
            bot.send_message(message.chat.id, 'Неверно. Сумма не может быть отрицательной!')
            bot.register_next_step_handler(message, summa)

    except ValueError:
        bot.send_message(message.chat.id, 'Неверно. Требуется ввести число!')
        bot.register_next_step_handler(message,summa_next)

def step_on(message):
    choice = adek(message.text)
    curs = ExchangeRates(str(date.today()))

    if choice == 'доллар':
        result = curs['USD']
        text = str(date.today()) +'\n'
        text += '⭐️ Курс доллара составляет ' + str(result.value) + ' RUB' +'\n'
        text += '💸 Введенная сумма составляет ' + str(round(result.value * amount)) + ' RUB'
        bot.send_message(message.chat.id, text)

        markup = types.ReplyKeyboardMarkup()
        but1 = types.InlineKeyboardButton('перевести еще')
        but2 = types.InlineKeyboardButton('главное меню')

        markup.add(but1, but2)
        bot.send_message(message.chat.id, 'Что теперь?', reply_markup=markup)

        bot.register_next_step_handler(message, step_on1)


    elif choice == 'евро':
        result = curs['EUR']
        text = str(date.today()) + '\n'
        text += '⭐️ Курс евро составляет ' + str(result.value) + ' RUB'  +'\n'
        text += '💸 Введенная сумма составляет ' + str(round(result.value * amount)) + ' RUB'

        bot.send_message(message.chat.id, text)

        markup = types.ReplyKeyboardMarkup()
        but1 = types.InlineKeyboardButton('перевести еще')
        but2 = types.InlineKeyboardButton('главное меню')

        markup.add(but1, but2)
        bot.send_message(message.chat.id, 'Что теперь?', reply_markup=markup)
        bot.register_next_step_handler(message, step_on1)


    elif choice == 'юань':
        result = curs['CNY']
        a = str(result.value)
        text = str(date.today()) + '\n'
        text += '⭐ Курс юаня составляет ' + a + ' RUB'  +'\n'
        text += '💸 Введенная сумма составляет ' + str(round(result.value * amount)) + ' RUB'

        bot.send_message(message.chat.id, text)

        markup = types.ReplyKeyboardMarkup()
        but1 = types.InlineKeyboardButton('перевести еще')
        but2 = types.InlineKeyboardButton('главное меню')

        markup.add(but1, but2)
        bot.send_message(message.chat.id, 'Что теперь?', reply_markup=markup)

        bot.register_next_step_handler(message, step_on1)


    elif choice == 'фунт':
        result = curs['GBP']
        text = str(date.today()) + '\n'
        text += '⭐ Курс фунта составляет ' + str(result.value) + ' RUB'  +'\n'
        text += '💸 Введенная сумма составляет ' + str(round(result.value * amount)) + ' RUB'

        bot.send_message(message.chat.id, text)

        markup = types.ReplyKeyboardMarkup()
        but1 = types.InlineKeyboardButton('перевести еще')
        but2 = types.InlineKeyboardButton('главное меню')

        markup.add(but1, but2)
        bot.send_message(message.chat.id, 'Что теперь?', reply_markup=markup)

        bot.register_next_step_handler(message, step_on1)

    elif choice == 'главное меню':
        quit(message)

    elif choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)

    else:
        bot.send_message(message.chat.id, 'Неверно - воспользуйся кнопками!')
        summa_next(message)
def step_on1(message):
    choice = adek(message.text)
    if choice == 'перевести еще':
        summa(message)

    elif choice == 'главное меню':
        quit(message)

    elif choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)

    else:
        bot.send_message(message.chat.id, 'Неверно - воспользуйся кнопками!')
        summa(message)


#блок 8
def help(message):
    markup = types.ReplyKeyboardMarkup()
    but1 = types.InlineKeyboardButton('что ты умеешь?')
    but2 = types.InlineKeyboardButton('главное меню')
    markup.add(but1, but2)

    bot.send_photo(message.chat.id, get('https://medialeaks.ru/wp-content/uploads/2020/06/annotacziya-2020-06-11-143333.jpg').content)

    bot.send_message(message.chat.id, 'Выбери кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, step_on2)

def step_on2(message):
    choice = adek(message.text)
    if choice =='главное меню':
        quit(message)
    elif choice == 'что ты умеешь?':
        text = 'Я - бот, и я был создан, чтобы ' +'\n'
        text += 'помочь с некоторыми задачами' +'\n'
        text += '' +'\n'
        text += 'Я умею:'+'\n'
        text += '🍄 Показывать погоду в любом выбранном городе' +'\n'
        text += ''+'\n'
        text += '🍄 Переводить доллары, евро, фунты и юани в рубли '+'\n'
        text += '- обратно пока не умею, но скоро научусь' +'\n'
        text += '' +'\n'
        text += '🍄 Показывать список твоих дедлайнов, '  +'\n'
        text += 'которые ты можешь редактировать,' +'\n'
        text += 'удаляя и добавляя новые' '\n'


        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, step_on3)

    elif choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)


def step_on3(message):
    choice = adek(message.text)
    if choice == 'главное меню':
        quit(message)
    elif choice == 'что ты умеешь?':
        step_on2(message)

    elif choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)

    else:
        bot.send_message(message.chat.id, 'Ошибка, воспользуйся кнопками')
        bot.register_next_step_handler(message, step_on2)

#блок 9
@bot.message_handler(commands=['text'])
def dead(message):

        knop = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton('добавить дедлайн')
        but2 = types.KeyboardButton('удалить дедлайны')
        but3 = types.KeyboardButton('показать дедлайны')
        but4 = types.KeyboardButton('главное меню')

        knop.add(but1, but2, but3, but4)
        bot.send_photo(message.chat.id, get('https://i.pinimg.com/564x/df/e6/fd/dfe6fd9d64c7702febd24e50153525e3.jpg').content)

        bot.send_message(message.chat.id, 'Что требуется сделать?', reply_markup=knop)

        bot.register_next_step_handler(message, dead1)


def dead1(message):
    connection = sqlite3.connect('dead.sql')
    connect = connection.cursor()

    connect.execute('CREATE TABLE IF NOT EXISTS tasks (id int auto_increment primary key, date varchar(15), task varchar (50))')

    connection.commit()
    connect.close()
    connection.close()

    choice = adek(message.text)
    if choice == 'добавить дедлайн':
        bot.send_message(message.chat.id, 'Введи задачу')
        bot.register_next_step_handler(message, dead2)

    elif choice == 'показать дедлайны':
        show(message)

    elif choice == 'удалить дедлайн':
        delete(message)


    elif choice == 'главное меню':
        quit(message)

    elif choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)

    else:
        bot.send_message(message.chat.id, mistake_text)
        dead(message)

def dead2(message):
    global task
    task = adek(message.text)


    bot.send_message(message.chat.id, 'Введи дату дедлайна')
    bot.register_next_step_handler(message, dead3)


def dead3(message):
    date = adek(message.text)

    connection = sqlite3.connect('dead.sql')
    connect = connection.cursor()


    connect.execute(f'INSERT INTO tasks (task, date) VALUES ("{task}", "{date}")')

    connection.commit()
    connect.close()
    connection.close()

    bot.send_message(message.chat.id, 'задача добавлена!')


    knop = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('добавить еще дедлайн')
    but2 = types.KeyboardButton('удалить дедлайн')
    but3 = types.KeyboardButton('показать дедлайны')
    but4 = types.KeyboardButton('главное меню')

    knop.add(but1, but2, but3, but4)
    bot.send_message(message.chat.id, 'Что теперь?', reply_markup=knop)

    bot.register_next_step_handler(message, dead4)


def dead4(message):
    choice = adek(message.text)
    if choice =='добавить дедлайн' or choice =='удалить дедлайн'  or choice == 'показать дедлайны':
        dead1(message)
    elif choice =='главное меню':
        quit(message)

    elif choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)

    else:
        bot.send_message(message.chat.id, 'Ошибка, попробуй воспользоваться кнопками')
        bot.register_next_step_handler(message, dead)


@bot.callback_query_handler(func=lambda call: True)
def show(message):
    try:
        connection = sqlite3.connect('dead.sql')
        connect = connection.cursor()

        connect.execute('SELECT * FROM tasks')

        tasks = connect.fetchall()

        text = ''
        a = 'Твои дедлайны' + '\n'
        k = ''
        a = a+k

        b = connect.execute("select count(*) from tasks")
        c = connect.fetchone()

        for i in range(1, int(c[0]) + 1):
            for el in tasks:

                if el[1] != '':
                    if not(str(i)+') ' in text):
                        if not (str(el[1]) in text):
                            text +=  f'{str(i) + ") " + el[1]+ " - "}{el[2]} \n'


        connect.close()
        connection.close()
        bot.send_message(message.chat.id, a)
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, dead4)

    except Exception:
        bot.send_message(message.chat.id, 'Дедлайнов нет. Самое время добавить новые')
        dead(message)

@bot.message_handler(commands=['text'])
def delete(message):
    knop = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('очистить дедлайны')
    but2 = types.KeyboardButton('назад')


    knop.add(but1, but2)
    bot.send_message(message.chat.id, 'Что ты хочешь сделать?',reply_markup=knop)
    bot.register_next_step_handler(message, delete1)

def delete1(message):
    choice = adek(message.text)
    if choice == 'очистить дедлайны':
        conn = sqlite3.connect('dead.sql')
        cur = conn.cursor()

        cur.execute('DELETE FROM tasks;')
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, 'Супер! - все дедлайны очищены')
        dead(message)

    elif choice =='назад':
        dead(message)

    elif choice == '/start':
        bot.send_message(message.chat.id, 'Сейчас бот будет перезапущен!')
        user(message)



bot.polling(none_stop=True)

