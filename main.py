import telebot
import requests
import random
from telebot import types
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN =os.environ.get("BOT_TOKEN")
WEATHER_API = os.environ.get("WEATHER_API")
bot = telebot.TeleBot(BOT_TOKEN)
bot1 = os.environ.get("WEATER_API")
questions = [
    {"question": "2 + 2 =", "options": ["3", "4", "5"], "correct_answer": "4"},
    {"question": "8 * 3 =", "options": ["21", "24", "28"], "correct_answer": "24"},
    {"question": "15 - 7 =", "options": ["6", "8", "10"], "correct_answer": "8"},
    {"question": "3 * 7 =", "options": ["21", "24", "26"], "correct_answer": "21"},
    {"question": "8 * 6 =", "options": ["44", "48", "47"], "correct_answer": "48"},
    {"question": "9 * 5 =", "options": ["45", "40", "43"], "correct_answer": "21"},
    {"question": "6 * 7 =", "options": ["46", "43", "42"], "correct_answer": "21"},
    {"question": "4 * 6 =", "options": ["21", "24", "26"], "correct_answer": "24"},
    {"question": "7 * 7 =", "options": ["48", "49", "47"], "correct_answer": "21"},
    {"question": "8 * 4 =", "options": ["38", "34", "32"], "correct_answer": "32"},
]

user_scores = {}

def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/quiz')
    markup.add(itembtn1)
    bot.reply_to(message, "Assalomu alaykum! Matematika botiga xush kelibsiz. Savollar uchun /quiz buyrug'ini kiriting.", reply_markup=markup)

def send_question(message):
    chat_id = message.chat.id

    if chat_id not in user_scores or (user_scores[chat_id]["correct"] + user_scores[chat_id]["incorrect"]) >= 10:
        user_scores[chat_id] = {"correct": 0, "incorrect": 0, "asked_questions": []}

    available_questions = [q for q in questions if q not in user_scores[chat_id]["asked_questions"]]
    if not available_questions:
        user_scores[chat_id]["asked_questions"] = []
        available_questions = questions

    question = random.choice(available_questions)
    user_scores[chat_id]["current_question"] = question
    user_scores[chat_id]["asked_questions"].append(question)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for option in question["options"]:
        markup.add(types.KeyboardButton(option))

    bot.send_message(chat_id, f"{question['question']}", reply_markup=markup)

def check_answer(message):
    chat_id = message.chat.id
    user_answer = message.text.strip()

    if chat_id in user_scores:
        question = user_scores[chat_id]["current_question"]
        correct_answer = question["correct_answer"]

        if user_answer == correct_answer:
            user_scores[chat_id]["correct"] += 1
        else:
            user_scores[chat_id]["incorrect"] += 1

        if (user_scores[chat_id]["correct"] + user_scores[chat_id]["incorrect"]) == 10:
            bot.send_message(chat_id, f"Siz 10 savoldan {user_scores[chat_id]['correct']} ta to'g'ri, {user_scores[chat_id]['incorrect']} ta noto'g'ri javob berdingiz.")
            send_welcome(message)
        elif (user_scores[chat_id]["correct"] + user_scores[chat_id]["incorrect"]) < 10:
            send_question(message)

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    send_welcome(message)

@bot.message_handler(commands=['quiz'])
def handle_quiz(message):
    send_question(message)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    check_answer(message)

if __name__ == "__main__":
    bot.polling(none_stop=True)