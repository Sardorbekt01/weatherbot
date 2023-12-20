import telebot
import requests
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN =os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    bot.reply_to(message,
                 f"Assalomu, {user.first_name}! botimizga xush kelibsiz 😊.\nBu botdan siz ob-havo malumotlarini bilib olishingiz mumkin.\n /help buyrug'ini bering.")

# /help buyrug'iga javob berish
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Men yordam qilaman!")

@bot.message_handler(commands=['weather'])
def get_weather(message):
    city = message.text[9:]
    data = get_full_data(city)
    temp = round(data.get("main", {}).get('temp', 0) - 273.15)
    speed = data.get("wind",{}).get('speed',0)
    cloud = data.get("wind",{}).get('speed')
    bot.send_message(message.chat.id, f"hozirda {city}da havo {temp} bo'lishi kutulmoqda!\nShamol {speed}m/s tezlikka esadi.\nOsmonda {cloud} kutilmoqda")

# @bot.message_handler(func = lambda msg: True)
# def reply_msg(message):
#     bot.send_message(message.chat.id, message.text)
#     # bot.reply_to(message, str(message.chat.id))

def get_full_data(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?appid=78a2e76d709d1222a5487dd5ad41b74b={}'.format(city)
    response = requests.get(url)
    return response.json()


bot.infinity_polling()