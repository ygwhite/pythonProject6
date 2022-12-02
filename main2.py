
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as bs
from sell import selling
# from parsing import libs, libs_image
# from Parsing_game_link import standart_data, max_data

bot = telebot.TeleBot('5349217968:AAE8sUNG8U2fxQtPg5RaniG1Z9s7Q6tjcbc')
url = 'https://store.playstation.com/en-tr/pages/browse/'
my_link = 'https://t.me/dzinsakay'
my_card = '2200700126570885'
https_proxy = "66.23.233.90: 3128"
http_proxy = "37.235.48.19:80"
proxies = {
    "http": http_proxy,
    "https": https_proxy,
}


#парсинг

ps_list_game = []
ps_link_game = []
ps_image_game = []

for page in range(1, 20):
    url = f'https://store.playstation.com/en-tr/pages/browse/{page}'
    r = requests.get(url, proxies=proxies)
    soup = bs(r.text, 'html.parser')
    for ps_game in soup.find_all('li', class_='psw-l-w-1/2@mobile-s psw-l-w-1/2@mobile-l psw-l-w-1/6@tablet-l psw-l-w-1/4@tablet-s psw-l-w-1/6@laptop psw-l-w-1/8@desktop psw-l-w-1/8@max'):
        ps_list_game.append(ps_game.text)
    for link in soup.find_all('a', class_='psw-link psw-content-link'):
        ps_link_game.append('https://store.playstation.com' + link.get('href'))
    for image in soup.find_all('img',class_='psw-blur psw-top-left psw-l-fit-cover'):
        image_link = image.get('src')
        image_s_link = image_link.replace('?w=54&thumb=true', ' ')
        ps_image_game.append(image_s_link)
def flatten(xss):
    return [x for xs in xss for x in xs]

libs = dict(zip(ps_list_game, ps_link_game))
libs_image = dict(zip(ps_list_game, ps_image_game))

#парсинг



#game link


def max_data(url):
    r = requests.get(url, proxies=proxies)
    soup = bs(r.text, 'lxml')
    try:
        name_max_edition = [x.text for x in soup.find_all('h3',class_='psw-t-title-s psw-t-align-c psw-fill-x psw-p-t-6 psw-p-x-7')]
        sell_max_edition = []
        for sel in soup.find_all('span', class_='psw-t-title-m')[1:]:
            if sel.text == 'Included' or sel.text == 'Game Trial' or sel.text == 'Free':
                continue
            else:
                sell_max_edition.append(selling(sel.text))
        libs_sell_and_name = list(zip(sell_max_edition, name_max_edition))
        max_edition_sell_and_name = max(libs_sell_and_name)
        return max_edition_sell_and_name
    except:
        print('none')

def standart_data(url):
    r = requests.get(url, proxies=proxies)
    soup = bs(r.text, 'lxml')
    game_ps5_sell = soup.find_all('span', class_='psw-t-title-m')[0].text
    return game_ps5_sell


#game_link
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    play = types.KeyboardButton('/play')
    sub = types.KeyboardButton('/sub')
    markup.add(play, sub)
    bot.send_message(message.chat.id,
                     f'Привет,{message.from_user.first_name}\nТы хочешь подписку или игру? Если игру ,то нажми "/play" ,а если подписку ,то нажмите "/sub"',
                     reply_markup=markup)


@bot.message_handler(commands=['play'])
def bot_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('/back')
    markup.add(back)
    game_name = bot.send_message(message.chat.id, f'*Введите название игры:*', reply_markup=markup,
                                 parse_mode='Markdown')
    bot.register_next_step_handler(game_name, game_search)


def game_search(message):
    game_data = message.text
    i = False
    isfound = False
    for key, value in libs_image.items():
        if game_data.lower() in key.lower():
            img = value
            for key, value_link in libs.items():
                if game_data.lower() in key.lower():
                    i = True
                    isfound = True
                    r = requests.get(value_link, proxies=proxies)
                    soup = bs(r.text, 'lxml')
                    try:
                        name_game_ps5 = soup.find('h1',
                                                  class_='psw-m-b-5 psw-t-title-l psw-t-size-8 psw-l-line-break-word').text
                        # bot.send_message(message.chat.id,
                        #                  'Вы неправильно ввели название игры или я её не нашёл,может скините мне ссылку на игру? Нажмите "/link"')

                        bot.send_message(message.chat.id, f'[{name_game_ps5}]({img})', parse_mode='Markdown')
                        game_ps5_sell = soup.find_all('span', class_='psw-t-title-m')[0].text
                        print(game_ps5_sell)
                        if game_ps5_sell == 'Included' or game_ps5_sell == 'Game Trial' or game_ps5_sell == 'Free':
                            bot.send_message(message.chat.id, 'Игра бесплатная или демоверсия')
                        # else:
                        #     bot.send_message(message.chat.id, f'*1) Цена за стандартное издание PS5 = {selling(game_ps5_sell)}*', parse_mode='Markdown')
                    except Exception:
                        continue

                    try:
                        name_max_edition = [x.text for x in soup.find_all('h3',
                                                                          class_='psw-t-title-s psw-t-align-c psw-fill-x psw-p-t-6 psw-p-x-7')]
                        sell_max_edition = []
                        for sel in soup.find_all('span', class_='psw-t-title-m')[1:]:
                            if sel.text == 'Included' or sel.text == 'Game Trial' or sel.text == 'Free':
                                continue
                            else:
                                sell_max_edition.append(selling(sel.text))
                        print(sell_max_edition, '\n', name_max_edition)
                        libs_sell_and_name = list(zip(sell_max_edition, name_max_edition))
                        print(libs_sell_and_name)
                        max_edition_sell_and_name = max(libs_sell_and_name)
                        print(max_edition_sell_and_name)
                        bot.send_message(message.chat.id,
                                         f'*{max_edition_sell_and_name[1]} = {max_edition_sell_and_name[0]}*',
                                         parse_mode='Markdown')
                    except Exception:
                        bot.send_message(message.chat.id,
                                         'Вы неправильно ввели название игры ,может скините мне ссылку на игру? Нажмите "/link"')
                if i == True:
                    break
            if i == True:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                bot.send_message(message.chat.id, '*Если это не та игра ,которую вы ищите ,то нажмите "/link"*',
                                 parse_mode='Markdown')
                bot.send_message(message.chat.id, '*Для оплаты нажмите "/pay"*', reply_markup=markup,
                                 parse_mode='Markdown')
                bot.send_message(message.chat.id, f'[Поддержка]({my_link})', parse_mode='Markdown')
                break
    if isfound == False:
        bot.send_message(message.chat.id,
                         'Вы неправильно ввели название игры ,может скините мне ссылку на игру? Нажмите "/link"')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('/back')
    markup.add(back)


@bot.message_handler(commands=['sub'])
def sub(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('/back')
    markup.add(back)
    bot.send_message(message.chat.id, '1) PlayStation Plus DELUXE - 2100(год)')
    bot.send_message(message.chat.id, '2) PlayStation Plus EXTRA - 1900(год)')
    bot.send_message(message.chat.id, '3) PlayStation Plus ESSENTIAL - 1200 руб(год)')
    bot.send_message(message.chat.id, 'Если готовы купить ,нажмите /pay', reply_markup=markup)


@bot.message_handler(commands=['back'])
def back(message):
    return start(message)


@bot.message_handler(commands=['pay'])
def pay(message):
    bot.send_message(message.chat.id,
                     f'Оплата в данный момент недоступна',
                     parse_mode='Markdown')
    # bot.send_message(message.chat.id,f'Карта: {my_card} - Tinkoff')


@bot.message_handler(commands=['link'])
def link(message):
    try:
        game_link = bot.send_message(message.chat.id, f'Кидайте ссылку на игру с [сайта]({url})', parse_mode='Markdown')
        bot.register_next_step_handler(game_link, link_data)
    except Exception:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Неверная ссылка, ещё раз?', reply_markup=markup)


def link_data(message):
    try:
        if message.text == '/back':
            return start(message)
        else:
            link_data_ = message.text
            standart = standart_data(link_data_)
            max_ed = max_data(link_data_)
            img = message.text
            bot.send_message(message.chat.id, f'[Ваша игра]({img})', parse_mode='Markdown')
            bot.send_message(message.chat.id, f'*1) Цена за стандартное издание PS5 = {selling(standart)}*',
                             parse_mode='Markdown')
            bot.send_message(message.chat.id, f'*2) {max_ed[1]} = {max_ed[0]}*', parse_mode='Markdown')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id, 'Для оплаты нажмите "/pay"', reply_markup=markup)
            bot.send_message(message.chat.id, f'[Поддержка]({my_link})', parse_mode='Markdown')
    except Exception:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Неверная ссылка, ещё раз?', reply_markup=markup)
        bot.send_message(message.chat.id, f'[Поддержка]({my_link})', parse_mode='Markdown')
        return link(message)


bot.polling(none_stop=True)
