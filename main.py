from aiogram import Bot, Dispatcher, executor, types
import logging
from pyowm import OWM
from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime
from random import randint
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

bot = Bot(token="5265852488:AAESJ4IyBjYbSdxmuhk36KPufTVmuLfKaZU")
dp = Dispatcher(bot)
p2p = QiwiP2P(auth_key="eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Im84ZXBoay0wMCIsInVzZXJfaWQiOiI3OTUwNzE3ODY3MyIsInNlY3JldCI6IjhiZGY5ZjZmZTcyNWMxZjBiMzE0ZmViNGZkZGQxZjk4YjA1MjRjZTc4NGUyM2E5YjZkMmE5MzgzZmRiYzAxM2MifX0=")

def donate(amount):
    lifetime = 15 
    comment = 'На развитие' 
    bill = p2p.bill(amount=amount, lifetime=lifetime, comment=comment, bill_id=randint(1, 100000000)) 
    return f'Сумма: {amount}\nСсылка живет: {lifetime} минут\nСсылка:\n{bill.pay_url}'



def get_weather(city):
    try:
        owm = OWM('75b6b6bf8c7775c44dc00cb28f622ea8')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        w = observation.weather
        t = w.temperature('celsius')
        t1 = t['temp']
        t2 = t['feels_like']
        st = w.status
        if st == 'Rain':
            st = 'дождь'
        elif st == 'Clouds':
            st = 'облачно'
        elif st == 'Snow':
            st = 'снег'
        elif st == 'Fog' or st == 'Mist':
            st = 'туман'
        elif st == "Clear":
            st = 'ясно'
        elif 'light' in st:
            wth = st.split()[1]
            if wth == 'rain':
                st = 'слабый дождь'
            if wth == 'snow':
                st = 'слабый снег'
        else:
            st = st + "(ещё не переведено)"
        ans = "В городе {0} {1}, температура {2}, ощущается как {3}".format(
            city, st, t1, t2)
        return ans
    except Exception as e:
        return "Проверьте правильность написания региона или команды"

btn_weather = "⛅Погода⛅"
btn_donate = "$ Донатик на развитие $"
start_menu = ReplyKeyboardMarkup(resize_keyboard=True)
start_menu.add(btn_donate, btn_weather)
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет! Я Погодный Бот! Я знаю погоду в городах! Напишите команду: 'Погода <город>'(без кавычек) для получения прогноза", reply_markup=start_menu)

@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == "? Информация ?":
        await bot.send_message(message.from_user.id, "Привет! Я бот")
    if "погода" in message.text.lower() and len(message.text.lower().split()) > 1:
        city = message.text.lower().replace("погода", "").strip()
        await bot.send_message(message.from_user.id, get_weather(city))
    if "/donate" in message.text.lower():
        amount = message.text.lower().replace("/donate", "").strip()
        await bot.send_message(message.from_user.id, donate(amount)+'\nСпасибо за донатик!')
    if message.text == "⛅Погода⛅":
        await bot.send_message(message.from_user.id, "Напишите команду: 'Погода <город>' (без кавычек) для получения прогноза")
    if message.text == "$ Донатик на развитие $":
        await bot.send_message(message.from_user.id, "Напишите команду: '/donate <сумма платежа>' чтобы поддержать меня денюжкой")
    



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    