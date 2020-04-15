import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
try:
    from tg_token import TOKEN
except ImportError:
    print('Файл с токеном не найден')
    TOKEN = ''


WAIT = 0
POEM = """Ты меня не любишь, не жалеешь,
Разве я немного не красив?
Не смотря в лицо, от страсти млеешь,
Мне на плечи руки опустив.
Молодая, с чувственным оскалом,
Я с тобой не нежен и не груб.
Расскажи мне, скольких ты ласкала?
Сколько рук ты помнишь? Сколько губ?
Знаю я — они прошли, как тени,
Не коснувшись твоего огня,
Многим ты садилась на колени,
А теперь сидишь вот у меня.
Пусть твои полузакрыты очи
И ты думаешь о ком-нибудь другом,
Я ведь сам люблю тебя не очень,
Утопая в дальнем дорогом.
Этот пыл не называй судьбою,
Легкодумна вспыльчивая связь,-
Как случайно встретился с тобою,
Улыбнусь, спокойно разойдясь.
Да и ты пойдешь своей дорогой
Распылять безрадостные дни,
Только нецелованных не трогай,
Только негоревших не мани.
И когда с другим по переулку
Ты пойдешь, болтая про любовь,
Может быть, я выйду на прогулку,
И с тобою встретимся мы вновь.
Отвернув к другому ближе плечи
И немного наклонившись вниз,
Ты мне скажешь тихо: "Добрый вечер…"
Я отвечу: "Добрый вечер, miss".
И ничто души не потревожит,
И ничто ее не бросит в дрожь,-
Кто любил, уж тот любить не может,
Кто сгорел, того не подожжешь.
""".split("\n")


def start(update, context):
    context.chat_data['line_n'] = 1
    update.message.reply_text("Добрый день! Я бот-литератор.\n"
                              "Я пришлю тебе строку из стихотворения, а ты продолжи следующей.\n"
                              "Подскажу, если ты что-то забыл :)\n"
                              "Итак, я начну.",
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(POEM[0])
    return WAIT


def check(update, context):
    line_n = context.chat_data["line_n"]
    line = POEM[line_n]
    if line == update.message.text:
        # update.message.reply_text(reply_markup=ReplyKeyboardRemove())
        line_n += 1
        if line_n == len(POEM):
            update.message.reply_text("Это последняя строка. \n"
                                      "С вами было приятно общаться! До свидания.")
            return ConversationHandler.END
        else:
            context.chat_data["line_n"] = line_n
            update.message.reply_text(POEM[line_n])
        line_n += 1
        print(line_n, len(POEM))
        if line_n >= len(POEM):
            update.message.reply_text("Это была последняя строка. \n"
                                      "С вами было приятно общаться! До свидания.")
            return ConversationHandler.END
        else:
            context.chat_data["line_n"] = line_n
            return WAIT
    else:
        update.message.reply_text(
            "Неверно :( "
            "Вы можете использовать команду /suphler, чтобы услышать подсказку\n"
            "Повторю строку: \n" + POEM[line_n - 1],
            reply_markup=ReplyKeyboardMarkup(
                [['/suphler']],
                resize_keyboard=True)
        )
        return WAIT


def suphler(update, context):
    line_n = context.chat_data["line_n"]
    line = POEM[line_n]
    update.message.reply_text("Подскажу.\n\n" + line)


def help(update, context):
    update.message.reply_text(
        "Отправьте /start, чтобы начать",
        reply_markup=ReplyKeyboardMarkup([
            ['/start']
        ], resize_keyboard=True, one_time_keyboard=True)
    )


def stop(update, context):
    update.message.reply_text("До свидания!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_chat_data=True)],

        states={
            WAIT: [
                CommandHandler('stop', stop),
                CommandHandler(
                    "suphler",
                    suphler,
                    pass_chat_data=True
                ),
                MessageHandler(
                    Filters.regex("^[^/]"),
                    check,
                    pass_chat_data=True
                )
            ]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, help))

    try:
        updater.start_polling()
        updater.idle()
    except telegram.error.TelegramError:
        print("Ошибка. Видимо, ваш провайдер блокирует запросы.")
        exit(1)


main()