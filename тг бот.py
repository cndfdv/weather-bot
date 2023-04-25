from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup
import requests
from deep_translator import GoogleTranslator
import datetime
from statistics import mean
import asyncio





bot = Bot(token='6231023524:AAHzyvFj6XAXxtKhwUjJdDNVY-F6In2IKd4', parse_mode="HTML")
dp = Dispatcher(bot)


forecast_now = types.KeyboardButton('Узнать прогноз погоды сейчас')
clothes = types.KeyboardButton('Что сегодня надеть')
forecast_5days = types.KeyboardButton('Прогноз погоды на 5 дней')
forecast_day = types.KeyboardButton('Прогноз погоды в нужный день')
forecast_every_day = types.KeyboardButton('Уведомление о погоде на день')
not_forecast_every_day = types.KeyboardButton('Отмена уведомлений о погоде на день')

markup = ReplyKeyboardMarkup().add(forecast_now).add(clothes).add(forecast_5days).add(forecast_day).add(forecast_every_day).add(not_forecast_every_day)


file1 = open('дни в году.txt', 'r', encoding='utf-8')
all_days = [str(i).strip() for i in file1]  
own_city = 0
file2 = open('города.txt', 'r', encoding='utf-8')
CITY = [str(i).strip() for i in file2]   
file3 = open('время.txt', 'r', encoding='utf-8')
all_time = [str(i).strip() for i in file3]   
month = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global user_id
    user_id = message.from_user.id
    if message.from_user.first_name =='Elisey' and message.from_user.last_name == 'Badanin':
        mess = 'ганг или баньг лейм, или холд он, че решил погоду узнать чтобы тяги не пачкать?'
    elif message.from_user.first_name =='соня' and message.from_user.last_name == None:
        mess = 'привет, любовь моя'
    else:
        mess = f'Привет, {message.from_user.first_name} {message.from_user.last_name}👋, этот бот поможет узнать погоду, подскажет прогноз на день и во что можно одеться. Для начала работы напишите ваш город'
    await message.answer(mess)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("Вот функции этого бота, выбирайте", reply_markup=markup)


async def send_time_func(user_id):
    today1 = []
    n = []
    data_today1 = datetime.date.today()
    forecast_every_day = f'прогноз погоды на {str(datetime.date.today())[5:10]}\n'
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            today1 += i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description']
    except Exception as e: 
        await bot.send_message(user_id, 'В данный момент ведутся технические работы, бот недоступен для использования')
        pass
    for i in range(0, len(today1), 3):
        if i != len(today1) - 2:
            n.append(today1[i:i+3])
    for i in range(len(n) - 1):
        if n[i][0][:10] == str(data_today1):
            forecast_every_day += str(n[i][0]) + '\n' + str(n[i][1]) + ' ' + str(n[i][2]) + '\n'
            if str(n[i][0][8:10]) != str(n[i+1][0][8:10]):
                forecast_every_day += '\n'
    await bot.send_message(user_id, forecast_every_day)
    clothes1 = ''
    sr_temp1 = []
    osadki1 = ''
    data_today2  = datetime.date.today()
    today3 = []
    y = []
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            today3 += i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description']
    except Exception as e: 
        await bot.send_message(user_id, 'В данный момент ведутся технические работы, бот недоступен для использования')
        pass
    for i in range(0, len(today3), 3):
        if i != len(today3) - 2:
            y.append(today3[i:i+3])
    for i in range(len(y) - 1):
        if y[i][0][:10] == str(data_today2) and 7 <= int(y[i][0][11:13]) <= 22:
            sr_temp1.append(int(y[i][1]))
            osadki1 += str(str(y[i][2]))
    sred1 = round(mean(sr_temp1))
    if sred1 >= 25:
        clothes1 += f'сегодня очень жарко - {sred1}°, поэтому можно надеть шорты, кроссовки или шлепанцы, и футболку \n'
        if osadki1.count('дождь') != 0:
            clothes1 += 'Сегодня будет дождь, поэтому советую взять зонтик' 
    elif 15 <= sred1 < 25:
        clothes1 += f'сегодня довольно жарко - {sred1}°, поэтому можно надеть штаны или шорты, кроссовкии и  футболку с кофтой/ветровкой \n'
        if osadki1.count('дождь') != 0:
               clothes1 += 'Сегодня будет дождь, поэтому советую взять зонтик' 
    elif 10 <= sred1 < 15:
        clothes1 += f'сегодня прохладно - {sred1}°, поэтому можно надеть штаны, кроссовки и кофту с курткой/ветровкой \n'
        if osadki1.count('дождь') != 0:
            clothes1 += 'Сегодня будет дождь, поэтому советую взять зонтик' 
    elif 0 <= sred1 < 10:
        clothes1 += f'сегодня довольно холодно - {sred1}°, поэтому можно надеть штаны, кроссовки и кофту с курткой \n'
        if osadki1.count('дождь') != 0:
            clothes1 += 'Сегодня будет дождь, поэтому советую взять зонтик' 
    elif -10 <= sred1 < 0:
        clothes1 += f'сегодня холодно - {sred1}°, поэтому можно надеть штаны, теплые ботинки, кофту с пуховиком и шапку с шарфом'
    elif sred1 < -10:
        clothes1 += f'сегодня очень холодно - {sred1}°, поэтому можно надеть подштанники, штаны, теплые ботинки, кофту с пуховиком и шапку с шарфом'
    await bot.send_message(user_id, clothes1)


@dp.message_handler(text=CITY)
async def city(message: types.Message):
    global s_city
    global city_id
    global id
    global appid
    s_city = (GoogleTranslator(source='ru', target='en').translate(message.text)).capitalize()
    city_id = 0
    appid = "ebb7f668458b6491cb6fac9156aa38e6"
    id = message.chat.id
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find", params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        city_id = data['list'][0]['id']
        await message.answer('Отлично, чтобы ознакомиться с возможностями бота - напишите 🠖/help🠔')
    except Exception as e:
        await message.answer('К сожалению, у меня не получится предсказывать погоду для этого города')
        pass

@dp.message_handler(text="Узнать прогноз погоды сейчас")
async def forecast_now(message: types.Message):
    global temper
    global conditions
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        conditions = data['weather'][0]['description']
        temper = data['main']['temp']
    except Exception as e:
        await message.answer('В данный момент ведутся технические работы, бот недоступен для использования')
        pass
    await message.answer(f'погода сейчас в Вашем городе:\n температура - {round(int(temper))}°\n погода - {conditions}\n')


@dp.message_handler(text="Что сегодня надеть")
async def what_put_on(message: types.Message):
    clothes = ''
    sr_temp = []
    osadki = ''
    data_today  = datetime.date.today()
    today2 = []
    x = []
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            today2 += i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description']
    except Exception as e: 
        await message.answer('В данный момент ведутся технические работы, бот недоступен для использования')
        pass
    for i in range(0, len(today2), 3):
        if i != len(today2) - 2:
            x.append(today2[i:i+3])
    for i in range(len(x) - 1):
        if x[i][0][:10] == str(data_today) and 7 <= int(x[i][0][11:13]) <= 22:
            sr_temp.append(int(x[i][1]))
            osadki += str(str(x[i][2]))
    sred = round(mean(sr_temp))
    if sred >= 25:
        clothes += f'сегодня очень жарко - {sred}°, поэтому можно надеть шорты, кроссовки или шлепанцы, и футболку \n'
        if osadki.count('дождь') != 0:
            clothes += 'Сегодня будет дождь, поэтому советую взять зонтик' 
    elif 15 <= sred < 25:
        clothes += f'сегодня довольно жарко - {sred}°, поэтому можно надеть штаны или шорты, кроссовкии и  футболку с кофтой/ветровкой \n'
        if osadki.count('дождь') != 0:
            clothes += 'Сегодня будет дождь, поэтому советую взять зонтик' 
    elif 10 <= sred < 15:
        clothes += f'сегодня прохладно - {sred}°, поэтому можно надеть штаны, кроссовки и кофту с курткой/ветровкой \n'
        if osadki.count('дождь') != 0:
            clothes += 'Сегодня будет дождь, поэтому советую взять зонтик' 
    elif 0 <= sred < 10:
        clothes += f'сегодня довольно холодно - {sred}°, поэтому можно надеть штаны, кроссовки и кофту с курткой \n'
        if osadki.count('дождь') != 0:
            clothes += 'Сегодня будет дождь, поэтому советую взять зонтик' 
    elif -10 <= sred < 0:
        clothes += f'сегодня холодно - {sred}°, поэтому можно надеть штаны, теплые ботинки, кофту с пуховиком и шапку с шарфом'
    elif sred < -10:
        clothes += f'сегодня очень холодно - {sred}°, поэтому можно надеть подштанники, штаны, теплые ботинки, кофту с пуховиком и шапку с шарфом'
    await message.answer(clothes)


@dp.message_handler(text="Прогноз погоды на 5 дней")
async def forecast_five_days(message: types.Message):
    on5days = []
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            on5days += i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description']
    except Exception as e: 
        await message.answer('В данный момент ведутся технические работы, бот недоступен для использования')
        pass
    m = []
    for i in range(0, len(on5days), 3):
        if i != len(on5days) - 2:
            m.append(on5days[i:i+3])
    forecast5days = 'прогноз погоды на 5 дней\n'
    for i in range(len(m) - 1):
        forecast5days += str(m[i][0]) + '\n' + str(m[i][1]) + ' ' + str(m[i][2]) + '\n'
        if str(m[i][0][8:10]) != str(m[i+1][0][8:10]):
            forecast5days += '\n'
    forecast5days += str(m[-1][0]) + '\n' + str(m[-1][1]) + ' ' + str(m[-1][2]) + '\n'
    await message.answer(forecast5days)


@dp.message_handler(text="Прогноз погоды в нужный день")
async def forecast_need_day(message: types.Message):
    await message.answer('Укажите дату')


@dp.message_handler(text=all_days)
async def forecast_need_day_weather(message: types.Message):
    date = f'{nums[month.index(message.text.split()[1])]}-{message.text.split()[0]}'
    today = []
    l = []
    forecasttoday = f'прогноз погоды на {message.text}\n'
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            today += i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description']
    except Exception as e: 
        await message.answer('В данный момент ведутся технические работы, бот недоступен для использования')
        pass
    for i in range(0, len(today), 3):
        if i != len(today) - 2:
            l.append(today[i:i+3])
    for i in range(len(l) - 1):
        if l[i][0][5:10] == date:
            forecasttoday += str(l[i][0]) + '\n' + str(l[i][1]) + ' ' + str(l[i][2]) + '\n'
            if str(l[i][0][8:10]) != str(l[i+1][0][8:10]):
                forecasttoday += '\n'
    await message.answer(forecasttoday)


@dp.message_handler(text="Уведомление о погоде на день")
async def time_everyday_forecast(message: types.Message):
    await message.answer('Бот будет отправлять вам прогноз погоды на день в определенное время')
    await message.answer('Введите время в формате ЧЧ:ММ. В это время каждый день бот будет отправлять вам прогноз погоды на день')



@dp.message_handler(text=all_time)
async def creaate_send_time(message: types.Message):
    global send_time
    send_time = message.text
    user_id = message.from_user.id
    await message.answer(f'Теперь вы будете получать сообщение с прогнозом погоды и рекомендациями по выбору одежды каждый день в {send_time}')

    # Schedule the notification
    send_time = datetime.datetime.strptime(send_time, '%H:%M')
    now = datetime.datetime.now()
    send_time = datetime.datetime.combine(now.date(), send_time.time())
    delay = (send_time - now).total_seconds()

    asyncio.get_event_loop().call_later(delay, lambda: asyncio.create_task(send_time_func(user_id)))


@dp.message_handler(text="Отмена уведомлений о погоде на день")
async def creaate_send_time(message: types.Message):
    send_time = 0
    await message.answer(f'Вы больше не будете получать уведомления')


executor.start_polling(dp)