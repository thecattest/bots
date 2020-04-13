import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from tg_token import TOKEN


def stop(update, text):
    update.message.reply_text('Ну, значит в другой раз. Всего доброго!')
    return ConversationHandler.END


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?\n"
        "Вы можете пропустить этот вопрос, отправив команду /skip"
    )

    return 1


def skip(update, context):
    update.message.reply_text("Можно и так!\nКакая погода у вас за окном?")
    return 2


def first_response(update, context):
    locality = update.message.text
    update.message.reply_text(
        "Какая погода в городе {locality}?".format(**locals()))
    return 2


def second_response(update, context):
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.regex('^[^/]'), first_response), CommandHandler('skip', skip)],
            2: [MessageHandler(Filters.regex('^[^/]'), second_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    try:
        updater.start_polling()
        updater.idle()
    except telegram.error.TelegramError:
        print("Ошибка. Видимо, ваш провайдер блокирует запросы.")
        exit(1)


main()