import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from tg_token import TOKEN


ENTRANCE, FIRST_HALL, SECOND_HALL, THIRD_HALL, FOURTH_HALL = range(5)


def start(update, context):
    reply_keyboard = [['1 зал']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text("Добро пожаловать в музей! Пожалуйста, сдайте верхнюю одежду в гардероб!\n"
                              "Вы можете экстренно эвакуироваться, отправив команду /stop\n"
                              "Вы можете перейти в первый зал",
                              reply_markup=markup)
    return ENTRANCE


def first_hall(update, context):
    reply_keyboard = [['2 зал'],
                      ['/quit']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text("Вы перешли в первый зал.\n"
                              "Тут можно найти разные интересные штуки, названия которым я не придумал...\n"
                              "Вы можете перейти во второй зал\n"
                              "Выход из музея находится в первом зале",
                              reply_markup=markup)
    return FIRST_HALL


def second_hall(update, context):
    reply_keyboard = [['3 зал']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text("Вы перешли во второй зал.\n"
                              "Тут можно найти другие интересные штуки, названия которым я тоже пока не придумал...\n"
                              "Вы можете перейти в третий зал\n"
                              "Выход из музея находится в первом зале",
                              reply_markup=markup)
    return SECOND_HALL


def third_hall(update, context):
    reply_keyboard = [['4 зал', '1 зал']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text("Вы уже в третьем зале!\n"
                              "Тут находятся самые-самые интересные штуки, названия которым я до сих пор не придумал\n"
                              "Вы можете перейти в четвертый или первый зал\n"
                              "Выход из музея находится в первом зале",
                              reply_markup=markup)
    return THIRD_HALL


def fourth_hall(update, context):
    reply_keyboard = [['1 зал']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text("Вы перешли в последний, четвёртый зал.\n"
                              "Тут нет ничего интересного, уходите...\n"
                              "Вы можете перейти в первый зал\n"
                              "Выход из музея находится в первом зале",
                              reply_markup=markup)
    return FOURTH_HALL


def quit(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!", reply_markup=markup)
    return ConversationHandler.END


def stop(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text("Вы эвакуировались. Гардероб и все ваши вещи сгорели. Хорошего дня :)", reply_markup=markup)
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ENTRANCE: [MessageHandler(Filters.regex('1 зал'), first_hall)],

            FIRST_HALL: [MessageHandler(Filters.regex('2 зал'), second_hall),
                         CommandHandler('quit', quit)],

            SECOND_HALL: [MessageHandler(Filters.regex('3 зал'), third_hall)],

            THIRD_HALL: [MessageHandler(Filters.regex('4 зал'), fourth_hall),
                         MessageHandler(Filters.regex('1 зал'), first_hall)
                         ],
            FOURTH_HALL: [MessageHandler(Filters.regex('1 зал'), first_hall)],
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