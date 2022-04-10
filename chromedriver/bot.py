# Найди бота здесь
# t.me/dup_durup_dup_bot

import logging
import os

import telegram
from telegram.ext import (Updater, MessageHandler, Filters,
                          CommandHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup

from mangalib_parser import mangalib_parser
from mangapoisk_parser import parser_mangapoisk
from rulate_parser import rulate_parser
from ranobelib_parser import ranobelib_parser
from ranobe_novels_parser import ranobe_novels_parser


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5237678741:AAG9O-IJYkAH3TRlVqqyM5Td2sKWNwP6tsA'

reply_keyboard = [['/help', '/download']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def help(update, context):
    update.message.reply_text(
        open('data/text/help.txt', encoding='utf-8').read(),
        reply_markup=markup
    )


reply_kb_downloading = [['/help', '/download'],
                        ['/stop']]
markup_d = ReplyKeyboardMarkup(reply_kb_downloading, one_time_keyboard=False)


def download(update, context):
    update.message.reply_text(
        """Отправь ссылку на первую страницу главы манги или новеллы \n
(Например: https://mangapoisk.ru/manga/berserk/chapter/26-240)""",
        reply_markup=markup_d)
    return 1


def get_url(update, context):
    context.user_data['url'] = update.message.text
    url = context.user_data['url']
    if 'https://mangapoisk.ru' not in url and 'https://mangalib.me' not in url and\
            'https://tl.rulate.ru' not in url and 'https://ranobelib.me' not in url and\
            'https://ranobe-novels.ru' not in url:
        update.message.reply_text('Наверное вы ввели неверную ссылку~')
        return 1
    update.message.reply_text('Сколько глав скачать?')
    return 2


def download_manga(update, context):
    count = update.message.text
    try:
        count = int(count)
    except Exception:
        update.message.reply_text(
            """Введите число \n(1, 2, 3...)""")
        return 2
    url = context.user_data['url']
    # В данном случае боту нужно отправлять такое сообщение https://mangapoisk.ru/manga/berserk/chapter/26-240 3
    # 3 в этом сообщении - кол-во глав для загрузки
    # сделал просто для примера и теста
    # answer = update.message.text.split()
    # if len(answer) == 2:
    #     url, count = answer
    #     count = int(count)
    # elif len(answer) == 1:
    #     url = answer[0]
    #     count = 1

    """url = update.message.text
    update.message.reply_text('Сколько глав?')
    count = None
    while count:
        count = update.message.text
    update.message.reply_text(count)"""
    # if 'https://mangapoisk.ru' not in url and 'https://mangalib.me' not in url and\
    #         'https://tl.rulate.ru' not in url and 'https://ranobelib.me' not in url and\
    #         'https://ranobe-novels.ru' not in url:
    #     update.message.reply_text('Наверное вы ввели неверную ссылку~')
    #     return
    update.message.reply_text('Идет скачиваение...')
    if 'https://mangapoisk.ru' in url:
        zip_dir = parser_mangapoisk(url, count)
    elif 'https://mangalib.me' in url:
        zip_dir = mangalib_parser(url, count)
    elif 'https://tl.rulate.ru' in url:
        zip_dir = rulate_parser(url, count)
    elif 'https://ranobe-novels.ru' in url:
        zip_dir = ranobe_novels_parser(url, count)

    # elif 'ranobelib.me' in url:
    #     update.message.reply_text('1111')
    #     zip_dir = ranobelib_parser(url)
    #     update.message.reply_text('222222')
    else:
        update.message.reply_text('Наверное вы ввели неверную ссылку~')
        return 0
    try:
        context.bot.send_document(chat_id=update.message.chat_id, document=open(zip_dir, 'rb'))
    except Exception:
        update.message.reply_text('Что-то пошло не так')
        return 0
    # удаляем архив
    os.remove(zip_dir)
    # update.message.reply_text('Готово')
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("👋")
    return ConversationHandler.END


def main():
    # Создаём объект updater.

    updater = Updater(TOKEN)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    # text_handler = MessageHandler(Filters.text & ~Filters.command, download_manga)
    # Регистрируем обработчик в диспетчере.
    # dp.add_handler(text_handler)

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", help))

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /download. Она задаёт первый вопрос.
        entry_points=[CommandHandler('download', download)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, get_url)],
            # получает количество глав на скачивание и скачивает, отправляет архив
            2: [MessageHandler(Filters.text & ~Filters.command, download_manga)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop),
                   CommandHandler('download', download)]
    )

    dp.add_handler(conv_handler)


    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
