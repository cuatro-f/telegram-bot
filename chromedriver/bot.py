# Найди бота здесь
# t.me/dup_durup_dup_bot

import logging
import os

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup

from mangalib_parser import mangalib_parser
from mangapoisk_parser import parser_mangapoisk
from rulate_parser import rulate_parser
from ranobelib_parser import ranobelib_parser


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5237678741:AAG9O-IJYkAH3TRlVqqyM5Td2sKWNwP6tsA'


def download_manga(update, context):
    url = update.message.text
    update.message.reply_text('Сколько глав?')
    count = None
    while count:
        count = update.message.text
    update.message.reply_text(count)
    if 'https://mangapoisk.ru' not in url and 'https://mangalib.me' not in url and\
            'https://tl.rulate.ru' not in url and 'https://ranobelib.me' not in url:
        update.message.reply_text('Наверное вы ввели неверную ссылку~')
        return
    update.message.reply_text('Идет скачиваение...')
    if 'https://mangapoisk.ru' in url:
        zip_dir = parser_mangapoisk(url)
    elif 'https://mangalib.me' in url:
        zip_dir = mangalib_parser(url)
    elif 'https://tl.rulate.ru' in url:
        zip_dir = rulate_parser(url)
    elif 'ranobelib.me' in url:
        update.message.reply_text('1111')
        zip_dir = ranobelib_parser(url)
        update.message.reply_text('222222')
    else:
        update.message.reply_text('Наверное вы ввели неверную ссылку~')
        return
    try:
        context.bot.send_document(chat_id=update.message.chat_id, document=open(zip_dir, 'rb'))
    except Exception:
        update.message.reply_text('Что-то пошло не так')
        return
    # удаляем архив
    os.remove(zip_dir)
    # update.message.reply_text('Готово')


reply_keyboard = [['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def help(update, context):
    update.message.reply_text(
        open('data/text/help.txt', encoding='utf-8').read(),
        reply_markup=markup
    )


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
    text_handler = MessageHandler(Filters.text & ~Filters.command, download_manga)
    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", help))


    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
