import logging
import os
import sqlite3
import sys
from pprint import pprint

import pygame
import requests
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session import aiohttp
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters
from project_config import BOT_TOKEN
from telegram.ext import CommandHandler
bot = Bot(BOT_TOKEN, default=DefaultBotProperties())
logger = logging.getLogger(__name__)
dp = Dispatcher()
reply_keyboard = [['/start', '/help_command'],
                  ['/spisok_class_1', '/spisok_class_2'],
                  ['/spisok_class_3', '/schedule_class_1'],
                  ['/schedule_class_2', '/schedule_class_3'],
                  ['/map_Gimnazya1', '/map_Gimnazya2'],
                  ['/map_Gimnazya3', '/map_Lyceum1'],
                  ['/map_school16', '/map_Lyceum2'],
                  ['/map_school4']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
load_dotenv()
res_str = ''


def geocode(address):
    # Собираем запрос для геокодера.
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
        "geocode": address,
        "format": "json"}

    # Выполняем запрос.
    response = requests.get(geocoder_request, params=geocoder_params)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code} ({response.reason})""")

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def get_ll_spn(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = f"{dx},{dy}"

    return ll, span


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=markup)


async def help_command(update, context):
    await update.message.reply_text('/spisok_class_1 - вызывает список учеников 1 класса\n'
                                    '/spisok_class_2 - вызывает список учеников 2 класса\n'
                                    '/spisok_class_3 - вызывает список учеников 3 класса\n'
                                    '/schedule_class_1 - вызывает расписание на неделю 1 класса\n'
                                    '/schedule_class_2 - вызывает расписание на неделю 2класса\n'
                                    '/schedule_class_3 - вызывает расписание на неделю 3 класса\n'
                                    '/map_Lyceum1 - вызывает местоположение МБОУ "Лицей №1" на карте\n'
                                    '/map_Gimnazia1 - вызывает местоположение МБОУ "Гимназия №1" на карте\n'
                                    '/map_Gimnazia2 - вызывает местоположение МБОУ "Гимназия №2" на карте\n'
                                    '/map_Gimnazia3 - вызывает местоположение МБОУ "Гимназия №3" на карте\n'
                                    '/map_school16 - вызывает местоположение СОШ №16 на карте\n'
                                    '/map_school4 - вызывает местоположение СОШ №4 на карте\n')


async def spisok_class_1(update, context):
    query = """SELECT id, Student FROM Class1 WHERE id BETWEEN 0 AND 24"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    stroka = ''
    for i in result:
        stroka = str(i[0]) + ' - ' + i[1]
        f.write(f'{stroka}\n')
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = f.read()
    f.truncate(0)
    await update.message.reply_text(a)


async def spisok_class_2(update, context):
    query = """SELECT id, Student FROM Class2 WHERE id BETWEEN 0 AND 24"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    stroka = ''
    for i in result:
        stroka = str(i[0]) + ' - ' + i[1]
        f.write(f'{stroka}\n')
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = f.read()
    f.truncate(0)
    await update.message.reply_text(a)


async def spisok_class_3(update, context):
    query = """SELECT id, Student FROM Class3 WHERE id BETWEEN 0 AND 24"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    stroka = ''
    for i in result:
        stroka = str(i[0]) + ' - ' + i[1]
        f.write(f'{stroka}\n')
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = f.read()
    f.truncate(0)
    await update.message.reply_text(a)


async def schedule_class_1(update, context):
    query = """SELECT Понедельник, Вторник, Среда, Четверг, Пятница, Суббота  FROM Class1 WHERE id BETWEEN 0 AND 7"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    week = ['Понедельник: ', 'Вторник: ', 'Среда: ', 'Четверг: ', 'Пятница: ', 'Суббота: ']
    res = ''
    for i in range(len(result) - 1):
        stroka = ''
        for j in range(7):
            stroka += f'{result[j][i]} '
            print(stroka)
        res += f'{week[i]}{stroka}\n'
    f.write(res)
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = str(f.read())
    # print(a)
    f.truncate(0)
    await update.message.reply_text(a)


async def schedule_class_2(update, context):
    query = """SELECT Понедельник, Вторник, Среда, Четверг, Пятница, Суббота  FROM Class1 WHERE id BETWEEN 0 AND 7"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    week = ['Понедельник: ', 'Вторник: ', 'Среда: ', 'Четверг: ', 'Пятница: ', 'Суббота: ']
    res = ''
    for i in range(len(result) - 1):
        stroka = ''
        for j in range(7):
            stroka += f'{result[j][i]} '
            print(stroka)
        res += f'{week[i]}{stroka}\n'
    f.write(res)
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = str(f.read())
    # print(a)
    f.truncate(0)
    await update.message.reply_text(a)


async def schedule_class_3(update, context):
    query = """SELECT Понедельник, Вторник, Среда, Четверг, Пятница, Суббота  FROM Class1 WHERE id BETWEEN 0 AND 7"""
    con = sqlite3.connect('project_bd.sqlite')
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    f = open('bot.txt', mode='w', encoding='utf8')
    week = ['Понедельник: ', 'Вторник: ', 'Среда: ', 'Четверг: ', 'Пятница: ', 'Суббота: ']
    res = ''
    for i in range(len(result) - 1):
        stroka = ''
        for j in range(7):
            stroka += f'{result[j][i]} '
            print(stroka)
        res += f'{week[i]}{stroka}\n'
    f.write(res)
    f = open('bot.txt', mode='r+', encoding='utf8')
    a = str(f.read())
    # print(a)
    f.truncate(0)
    await update.message.reply_text(a)


async def map_Lyceum1(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Льва+Толстого+144'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Льва+Толстого+144')
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


async def map_Lyceum2(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Полющенкова+28+Б'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Полющенкова+28+Б')
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


async def map_Gimnazya1(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Бебеля+121'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Бебеля+121')
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


async def map_Gimnazya2(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Нариманова+65'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Нариманова+65')
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


async def map_Gimnazya3(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Академика+Королёва+5'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Академика+Королёва+5')
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


async def map_school16(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Зелёная+2+А'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Зелёная+2+А')
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


async def map_school4(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": 'Чистополь,+улица+Бутлерова+7+А'
    })
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn('Чистополь,+улица+Бутлерова+7+А')
    # Можно воспользоваться готовой функцией,
    # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.005,0.002&l=map"
    await context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="Нашёл:"
    )


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("map_Lyceum1", map_Lyceum1))
    application.add_handler(CommandHandler("map_Lyceum2", map_Lyceum2))
    application.add_handler(CommandHandler("map_Gimnazya2", map_Gimnazya2))
    application.add_handler(CommandHandler("map_Gimnazya1", map_Gimnazya1))
    application.add_handler(CommandHandler("map_Gimnazya3", map_Gimnazya3))
    application.add_handler(CommandHandler("map_school16", map_school16))
    application.add_handler(CommandHandler("map_school4", map_school4))
    application.add_handler(CommandHandler("help_command", help_command))
    application.add_handler(CommandHandler("spisok_class_1", spisok_class_1))
    application.add_handler(CommandHandler("spisok_class_2", spisok_class_2))
    application.add_handler(CommandHandler("spisok_class_3", spisok_class_3))
    application.add_handler(CommandHandler("schedule_class_1", schedule_class_1))
    application.add_handler(CommandHandler("schedule_class_2", schedule_class_2))
    application.add_handler(CommandHandler("schedule_class_3", schedule_class_3))
    application.run_polling()


if __name__ == '__main__':
    main()