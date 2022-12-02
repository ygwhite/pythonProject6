import telebot
from telebot import types

#from pay import pay
bot = telebot.TeleBot('5349217968:AAE8sUNG8U2fxQtPg5RaniG1Z9s7Q6tjcbc')
url = 'https://store.playstation.com/en-tr/pages/browse/'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    play = types.KeyboardButton('/play')
    sub = types.KeyboardButton('Подписку')
    markup.add(play, sub)
    bot.send_message(message.chat.id, f'Привет,{message.from_user.first_name}\nТы хочешь подписку или игру?',reply_markup=markup)
@bot.message_handler(commands=['play'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Игру':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.InlineKeyboardButton('Назад'))
            msg = bot.send_message(message.chat.id, '*Введите название игры:*', reply_markup=markup, parse_mode='Markdown')
            # bot.register_next_step_handler(msg, game_search)

        elif message.text == 'Подписку':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.InlineKeyboardButton('PlayStation Plus DELUXE - 2100(год)'))
            markup.add(types.InlineKeyboardButton('PlayStation Plus EXTRA - 1900(год)'))
            markup.add(types.InlineKeyboardButton('PlayStation Plus ESSENTIAL - 1200 руб(год)'))
            markup.add(types.InlineKeyboardButton('Назад'))
            bot.send_message(message.chat.id,'Доступные подписки: ', reply_markup=markup)
        elif message.text == 'Назад':
            start(message)
        elif message.text == 'Купить':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.InlineKeyboardButton('Оплачено!'))
            markup.add(types.InlineKeyboardButton('Назад'))



# def ser(message):
#     for key, value in libs.items():
#         if game == key:
#             bot.send_message(message.chat.id, value)

bot.polling(none_stop=True)