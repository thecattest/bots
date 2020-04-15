import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
try:
    from tg_token import TOKEN
except ImportError:
    print('Файл с токеном не найден')
    TOKEN = ''


def start(update, context):
    update.message.reply_text("OK.")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    updater.bot.set_webhook("https://telegram-yandex.herokuapp.com")

    dp.add_handler(MessageHandler(Filters.text, start))

    try:
        # updater.start_polling()
        updater.start_webhook()
        updater.idle()
    except telegram.error.TelegramError:
        print("Ошибка. Видимо, ваш провайдер блокирует запросы.")
        exit(1)


main()