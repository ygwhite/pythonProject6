import telebot
from telebot import types
from pars import libs, libs_image
import requests
from bs4 import BeautifulSoup as bs
from sell import  selling
bot = telebot.TeleBot('5349217968:AAE8sUNG8U2fxQtPg5RaniG1Z9s7Q6tjcbc')
url = 'https://store.playstation.com/en-tr/pages/browse/'
my_link = 'https://t.me/dzinsakay'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    play = types.KeyboardButton('/play')
    sub = types.KeyboardButton('Подписку')
    markup.add(play, sub)
    bot.send_message(message.chat.id, f'Привет,{message.from_user.first_name}\nТы хочешь подписку или игру?',reply_markup=markup)
@bot.message_handler(commands=['play'])
def bot_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton('Назад'))
    game_name = bot.send_message(message.chat.id, '*Введите название игры:*', reply_markup=markup, parse_mode='Markdown')
    bot.register_next_step_handler(game_name, game_search)
def game_search(message):
    if message.text == 'Назад':
        start(message)
    game_data = message.text
    for key, value in libs_image.items():
        if game_data == key:
            img = value
            bot.send_message(message.chat.id, f'[{game_data}]({img})', parse_mode='Markdown')
            for key, value_link in libs.items():
                if game_data == key:
                    r = requests.get(value_link)
                    soup = bs(r.text, 'lxml')
                    name_ps5_game = soup.find('h1', attrs={'data-qa': "mfe-game-title#name"}).text
                    sell_ps5_game = soup.find('span', class_='psw-t-title-m').text
                    print(sell_ps5_game)
                    bot.send_message(message.chat.id, name_ps5_game)
                    bot.send_message(message.chat.id, sell_ps5_game)



bot.polling(none_stop=True)