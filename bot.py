"""
Домашнее задание №1
Использование библиотек: ephem
* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход 
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите 
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите 
  бота отвечать, в каком созвездии сегодня находится планета.
"""
import logging, datetime
from glob import glob
from random import choice

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import ephem
from  emoji import emojize

import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


def greet_user(bot, update, user_data):
    text = 'Вызван /start'
    emo = emojize(choice(settings.USER_EMOJI), use_aliases = True)
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика']])
    user_data['emo'] = emo    
    text = 'Привет {}'.format(emo)
    update.message.reply_text(text, reply_markup=my_keyboard)

def talk_to_me(bot, update, user_data):
    user_text = "Привет {} {}! Ты написал: {}".format(update.message.chat.first_name, user_data['emo'],
                update.message.text)
    update.message.reply_text(user_text)
    
def check_constellation(bot, update):
    all_known_planets = ['Mars','Mercury','Jupiter','Neptune','Venus','Saturn','Uranus','Moon']
    planet_name = update.message.text.split()[1]
    if planet_name in all_known_planets:
        current_date = datetime.datetime.now()
        result_constellation = ephem.constellation(getattr(ephem,planet_name)(current_date))[1]
        update.message.reply_text(f'{planet_name} now in {result_constellation} constellation')
    else:
        update.message.reply_text("I know nothing about this planet")
 
def full_moon(bot, update):
    user_data = update.message.text.split()[1]
    next_full_moon_date = ephem.next_full_moon(user_data)
    update.message.reply_text(f'Следующее полнолуние {next_full_moon_date}')

def word_count(bot, update):
    user_text = update.message.text[10:]
    if user_text:
        for word in user_text.split():
            if word.isalpha() == False:
                update.message.reply_text('Строка должна содержать только буквы и пробелы')
                break
        else: 
            world_counter = len(user_text.split())
            update.message.reply_text(f'Строка содержит {world_counter} слов')
    else: 
        update.message.reply_text('Вы ничего не ввели')

def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jpg')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(cat_pic,'rb'))



def main():
    mybot = Updater(settings.API_KEY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", check_constellation))
    dp.add_handler(CommandHandler('next_full_moon', full_moon))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать кошечку)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()