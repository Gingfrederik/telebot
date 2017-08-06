import os
import logging

import telegram

from pymongo import MongoClient
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from google.cloud import speech
from db import url, adminlist

logging.basicConfig(filename='bot.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


client = MongoClient(url)
db = client['telebot']
user_collect = db['user']

def recog(filename):
    cmn = 'cmn-Hant-TW'
    en = 'en-US'
    speech_client = speech.Client()

    # Loads the audio into memory
    with open(filename, 'rb') as stream:
        audio_sample = speech_client.sample(
                stream=stream,
                encoding='LINEAR16',
                sample_rate_hertz=16000,
                )
        responses = audio_sample.streaming_recognize(language_code=cmn,single_utterance=True)
        results = list(responses)
        try:
            print(results[0].alternatives[0].transcript)
            return(results[0].alternatives[0].transcript)
        except:
            print('error')
            return('error')

def start(bot, update):
    user_id = update.message.from_user.id
    if not user_collect.find_one({"user_id":user_id}):
        post = {"user_id":user_id,
                "first_name":update.message.from_user.first_name,
                "last_name":update.message.from_user.last_name,
                "username":update.message.from_user.username
                }
        user_collect.insert_one(post)
    update.message.reply_text('Hello World!')

def hello(bot, update):
    update.message.reply_text(
        '閉嘴 {}'.format(update.message.from_user.first_name))

def fuck(bot, update):
    bot.send_photo(chat_id=update.message.chat_id, photo=open('photo/1.jpg', 'rb'))

def story(bot, update):
    bot.send_photo(chat_id=update.message.chat_id, photo=open('photo/3.jpg', 'rb'))

def sfuck(bot, update):
    bot.send_voice(chat_id=update.message.chat_id, voice=open('sound/fucksound.ogg', 'rb'))

def menu(bot, update):
    custom_keyboard = [['top-left', 'top-right'],
                                ['bottom-left', 'bottom-right']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                              text="Menu on",
                              reply_markup=reply_markup)

def menuoff(bot, update):
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(chat_id=update.message.chat_id,
                              text="Menu off",
                              reply_markup=reply_markup)

def admin(bot, update):
    user_id = update.message.from_user.id
    if user_id in adminlist:
        update.message.reply_text('Hi Admin')
    else:
        update.message.reply_text('Shut up')

def voice(bot, update):
    update.message.reply_text('GOT IT')
    file_id = update.message.voice.file_id
    newFile = bot.get_file(file_id)
    newFile.download('voice.ogg')
    os.system('sox "|opusdec --force-wav voice.ogg -" voice.wav')
    mess = recog('voice.wav')
    if mess =='error':
        update.message.reply_text('ERROR(你可能要在說一次)')
    else:
        update.message.reply_text(
            '你是說：{}'.format(mess))

updater = Updater(token='341044903:AAFEbQ1WtVfvmJbraZzpCza_6bwYKYCJr-c')


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('fuck', fuck))
updater.dispatcher.add_handler(CommandHandler('story', story))
updater.dispatcher.add_handler(CommandHandler('sfuck', sfuck))
updater.dispatcher.add_handler(CommandHandler('menu', menu))
updater.dispatcher.add_handler(CommandHandler('menuoff', menuoff))
updater.dispatcher.add_handler(CommandHandler('admin', admin))
updater.dispatcher.add_handler(MessageHandler(Filters.voice, voice))

updater.start_polling()
updater.idle()
