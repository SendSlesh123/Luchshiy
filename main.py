import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv, find_dotenv
from random import randint
load_dotenv(find_dotenv())
token = os.getenv('token')



bot = telebot.TeleBot(token, parse_mode='HTML')

session = {}
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    chatID = message.from_user.id
    session[chatID] = {'count' : 0, 'bot_message' : 0, 'num_question': 0}
    bot.reply_to(message, "Hi!")

    markup = ReplyKeyboardMarkup()
    markup.add('Привет', 'Ну здравсвуй')

    message_bot = bot.send_message(chatID, message.text, reply_markup= markup)
    session[chatID]['bot_message'] = message_bot.id
    bot.register_next_step_handler(message, second_func)

@bot.message_handler(commands=['test'])
def start_test(message):
    chatID = message.from_user.id
    message_bot = bot.send_message(chatID, "Здесь будет ваш вопрос и какие нибудь варианты ответа")

@bot.message_handler(commands=['command1'])
def send_message_dice(message):
    chatID = message.from_user.id
    bot_message = bot.send_dice(chatID, '🏀')
    print(bot_message.dice.value)

@bot.message_handler(commands=['command2'])
def send_message_welcome(message):
    chatID = message.from_user.id
    bot.send_sticker(chatID, 'CAACAgIAAxkBAAJjFWaCa7GRzJBn--B92cI7tnRuNdXAAAKcDgACLu5YSE3_-MWXQYD0NQQ' )

@bot.message_handler(commands=['command3'])
def send_message_document(message):
    chatID = message.from_user.id
    bot.send_audio(chatID, 'https://file-cdn.online/mobile-rington/_ld/41/4156_top-zvonok.ru__.mp3')

@bot.message_handler(commands=['command4'])
def send_message_buttons(message):
    chatID = message.from_user.id
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('text1', callback_data='one')
    button2 = InlineKeyboardButton('text2', callback_data='two')
    button3 = InlineKeyboardButton('text3', callback_data='three')
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(chatID, 'Кнопочки', reply_markup= markup)

@bot.message_handler(commands=['game'])
def send_message_game(message):
    chatID = message.from_user.id
    session[chatID]['rand'] = randint(1, 100)
    bot.send_message(chatID, 'Бот загадает число от 1 до 100. Ваша цель его отгадать. На выполнение даётся 3 попытки.')
    bot.register_next_step_handler(message, first_try)

def first_try(message):
    chatID = message.from_user.id
    if int(message.text) == session[chatID]['rand']:
        bot.send_message(chatID,'Вы отдагали число с первой попытки. ')
    elif int(message.text) > session[chatID]['rand']:
        bot.send_message(chatID, 'Вы ввели число больше загаданного. Осталось 2 попытки')
        bot.register_next_step_handler(message, second_try)
    elif int(message.text) < session[chatID]['rand']:
        bot.send_message(chatID, 'Вы ввели число меньше загаданного. Осталось 2 попытки')
        bot.register_next_step_handler(message, second_try)

def second_try(message):
    chatID = message.from_user.id
    if int(message.text) == session[chatID]['rand']:
        bot.send_message(chatID,'Вы отдагали число со второй попытки.')
    elif int(message.text) > session[chatID]['rand']:
        bot.send_message(chatID, 'Вы ввели число больше загаданного. Осталась 1 попытка.')
        bot.register_next_step_handler(message, third_try)
    elif int(message.text) < session[chatID]['rand']:
        bot.send_message(chatID, 'Вы ввели число меньше загаданного. Осталась 1 попытка.')
        bot.register_next_step_handler(message, third_try)

def third_try(message):
    chatID = message.from_user.id
    if int(message.text) == session[chatID]['rand']:
        bot.send_message(chatID,'Вы отдагали число с третьей попытки.')
    else:
        bot.send_message(chatID, 'Повезёт в другой раз.')
@bot.callback_query_handler(func=lambda callback:True)
def handle_callback(callback):
    chatID = callback.from_user.id
    button_call = callback.data

    if button_call == 'one':
        bot.send_message(chatID, 'Вы нажали 1 кнопку')
    if button_call == 'two':
        bot.send_message(chatID, 'Вы нажали 2 кнопку')
    if button_call == 'three':
        bot.send_message(chatID, 'Вы нажали 3 кнопку')

@bot.message_handler(func=lambda message: True)
def first_func(message):
    chatID = message.from_user.id
    markup = ReplyKeyboardMarkup()
    # markup.add('Привет', 'Ну здравсвуй')
    #
    # message_bot = bot.send_message(chatID, message.text, reply_markup= markup)
    # session[chatID]['bot_message'] = message_bot.id
    # bot.register_next_step_handler(message, second_func)

def second_func(message):
    chatID = message.from_user.id
    bot.delete_message(chatID, session[chatID]['bot_message'])
    if message.text == 'Привет':
        bot.send_message(message.chat.id, "Привет!")
    elif message.text == 'Ну здравсвуй':
        bot.send_message(message.chat.id, "Удачной дороги, сталкер!")
    else:
        markup = ReplyKeyboardMarkup()
        markup.add('Привет', 'Ну здравсвуй')
        bot.send_message(message.chat.id, "Я тебя не понял. Повтори сообщение.")
        bot.register_next_step_handler(message, welcome)

def thirst_func(message):
    bot.send_message(message.chat.id, "какой то текст номер 2")



bot.infinity_polling()