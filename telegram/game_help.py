import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

import random
from tg_token import TOKEN


START, DICE, TIMER, WAIT = range(4)

help_markup = ReplyKeyboardMarkup([
    ['/start']
], resize_keyboard=True)
start_markup = ReplyKeyboardMarkup([
    ['/dice', '/timer']
], resize_keyboard=True)
dice_markup = ReplyKeyboardMarkup([
    ['/throw один 6-гранный'],
    ['/throw два 6-гранных'],
    ['/throw 20-гранный'],
    ['/cancel']
], resize_keyboard=True)
timer_markup = ReplyKeyboardMarkup([
    ['/set 30 секунд'],
    ['/set 1 минута'],
    ['/set 5 минут'],
    ['/cancel']
], resize_keyboard=True)
waiting_markup = ReplyKeyboardMarkup([
    ['/close']
], resize_keyboard=True)


def help_me(update, context):
    update.message.reply_text(
        "Отправьте /start, чтобы начать",
        reply_markup=help_markup
    )


def start(update, context):
    update.message.reply_text(
        "Привет! Я бот-помощник для игр.\n"
        "Я могу кинуть кубик по команде /dice или поставить таймер по команде /timer",
        reply_markup=start_markup
    )
    return START


def dice(update, context):
    update.message.reply_text(
        "Теперь выберите, какой кубик кинуть:",
        reply_markup=dice_markup
    )
    return DICE


def throw(update, context):
    type = context.args[0]
    if type == 'один':
        res = random.randint(1, 6)
    elif type == 'два':
        res = str(random.randint(1, 6)) + ' и ' + str(random.randint(1, 6))
    elif type == '20-гранный':
        res = random.randint(1, 20)
    else:
        return repeat(update, context)
    update.message.reply_text(
        f"Выпало {str(res)}. \nЕщё?",
        reply_markup=dice_markup
    )
    return DICE


def timer(update, context):
    update.message.reply_text(
        "Теперь выберите время",
        reply_markup=timer_markup
    )
    return TIMER


def set_timer(update, context):
    chat_id = update.message.chat_id
    due = context.args[0]
    print(due)
    if due == '30':
        time = 30
    elif due == '1':
        time = 60
    elif due == '5':
        time = 300
    else:
        return repeat(update, context)

    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()
    new_job = context.job_queue.run_once(task, time, context=chat_id)
    context.chat_data['job'] = new_job

    update.message.reply_text(
        f'Таймер на {time} секунд',
        reply_markup=waiting_markup
    )
    return WAIT


def wait(update, context):
    update.message.reply_text("Время ещё не вышло")
    return WAIT


def task(context):
    job = context.job
    context.bot.send_message(
        job.context, text='Время вышло.',
        reply_markup=timer_markup
    )
    return TIMER


def unset_timer(update, context):
    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']
    update.message.reply_text(
        'Таймер сброшен',
        reply_markup=timer_markup
    )
    return TIMER


def cancel(update, context):
    update.message.reply_text(
        "Окей, вы можете выбрать что-то другое.",
        reply_markup=start_markup
    )
    return START


def repeat(update, context):
    update.message.reply_text(
        "Не понял команду, давайте ещё разок",
        reply_markup=start_markup
    )
    return START


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            # предлагаем выбрать варинт развития событий
            START: [CommandHandler('dice', dice),
                    CommandHandler('timer', timer)],

            # выбираем, какой кубик кинуть
            DICE: [CommandHandler('cancel', cancel),
                   CommandHandler(
                        "throw",
                        throw,
                        pass_args=True
                    )],

            # выбираем время
            TIMER: [CommandHandler('cancel', cancel),
                    CommandHandler(
                        "set",
                        set_timer,
                        pass_args=True,
                        pass_job_queue=True,
                        pass_chat_data=True
                    )],

            WAIT: [CommandHandler('close', unset_timer),
                   MessageHandler(Filters.regex(".*"), wait)]
        },

        fallbacks=[CommandHandler('start', start),
                   MessageHandler(Filters.regex(".*"), repeat)]
    )
    dp.add_handler(conv_handler)

    dp.add_handler(MessageHandler(Filters.text, help_me))

    try:
        updater.start_polling()
        updater.idle()
    except telegram.error.TelegramError:
        print("Ошибка. Видимо, ваш провайдер блокирует запросы.")
        exit(1)


main()