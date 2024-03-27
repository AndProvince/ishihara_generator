# Ishihara Color Blindness Image Test Generator bot
# by Andrey Ponomarev
# 4ponomarev@gmail.com

import os
import telebot

from ishihara import create_image
from dotenv import load_dotenv

load_dotenv('settings.env')

BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    bot.reply_to(message, 'Hello!\n'
                          'Welcome to the Ishihara Color Blindness Image Test Generator.\n'
                          'I can convert your message into an Ishihara image.')


@bot.message_handler(content_types=['photo', 'document'])
def bot_message(message):
    bot.reply_to(message, 'Please send text message')


@bot.message_handler(content_types=['text'])
def photo(message):
    bot.reply_to(message, 'Ok, let\'s try.\n'
                          'Please wait a moment for the conversion "{}"'.format(message.text))

    bot.send_photo(message.chat.id, create_image(text=message.text))


if __name__ == '__main__':
    bot.infinity_polling()
