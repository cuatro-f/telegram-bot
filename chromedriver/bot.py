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

from data_db import db_session
from data_db.manga import Manga



db_session.global_init("db/catalog_manga.sqlite")

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5237678741:AAG9O-IJYkAH3TRlVqqyM5Td2sKWNwP6tsA'

reply_keyboard = [['/help'], ['/download_name', '/download_link']]
markup_start = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def help(update, context):
    update.message.reply_text(
        open('data/text/help.txt', encoding='utf-8').read(),
        reply_markup=markup_start
    )


reply_kb_downloading_link = [['/help', '/download_link'],
                        ['/stop']]
markup_d_l = ReplyKeyboardMarkup(reply_kb_downloading_link, one_time_keyboard=False)


def download_link(update, context):
    update.message.reply_text(
        """Отправь ссылку на первую страницу главы манги или новеллы \n
(Например: https://mangapoisk.ru/manga/berserk/chapter/26-240)""",
        reply_markup=markup_d_l)
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
        context.bot.send_document(
            chat_id=update.message.chat_id,
            document=open(zip_dir, 'rb'),
            reply_markup=markup_start
        )
    except Exception:
        update.message.reply_text('Что-то пошло не так')
        return 0
    # удаляем архив
    os.remove(zip_dir)
    # update.message.reply_text('Готово')
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text(
        "👋",
        reply_markup=markup_start
    )
    return ConversationHandler.END


reply_kb_downloading_name = [['/help', '/download_name'],
                        ['/stop']]
markup_d_n = ReplyKeyboardMarkup(reply_kb_downloading_name, one_time_keyboard=False)


def download_name(update, context):
    update.message.reply_text(
        open('data/text/download_name.txt', encoding='utf-8').read(),
        reply_markup=markup_d_n)
    return 1


def get_manga_name(update, context):
    context.user_data['name'] = update.message.text
    name = context.user_data['name'].lower()
    db_sess = db_session.create_session()
    manga = db_sess.query(Manga).filter(Manga.name.like(f'%{name}%')).all()
    # manga = db_sess.query(Manga).filter(name == Manga.name).first()
    if manga:
        if len(manga) > 1:
            context.user_data['manga'] = manga
            update.message.reply_text('Получилось найти несколько манг с похожим названием')
            show_links(update, context)
            return 3
        context.user_data['url'] = manga.url
        update.message.reply_text('Сколько глав скачать?')
        return 2
    else:
        update.message.reply_text(open('data/text/get_manga_name.txt', encoding='utf-8').read())
        return 1


def show_links(update, context):
    update.message.reply_text('Выберете номер нужной вам манги')
    out = list()
    manga = context.user_data['manga']
    for i in range(len(manga)):
        block = f'{i}: {manga[i].name}\n {manga[i].url}'
        out.append(block)
    out = '\n\n'.join(out)
    update.message.reply_text(out)


def get_need_link(update, context):
    ind_manga = update.message.text
    if not ind_manga.isdigit():
        update.message.reply_text('Введите число~')
        return 3
    ind_manga = int(ind_manga)
    context.user_data['url'] = context.user_data['manga'][ind_manga].url
    update.message.reply_text('Сколько глав скачать?')
    return 2


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

    conv_handler_link = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /download. Она задаёт первый вопрос.
        entry_points=[CommandHandler('download_link', download_link)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, get_url)],
            # получает количество глав на скачивание и скачивает, отправляет архив
            2: [MessageHandler(Filters.text & ~Filters.command, download_manga)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop),
                   CommandHandler('download_link', download_link)]
    )
    dp.add_handler(conv_handler_link)

    conv_handler_name = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /download. Она задаёт первый вопрос.
        entry_points=[CommandHandler('download_name', download_name)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, get_manga_name)],
            # получает количество глав на скачивание и скачивает, отправляет архив
            2: [MessageHandler(Filters.text & ~Filters.command, download_manga)],
            # 3: [MessageHandler(Filters.text & ~Filters.command, show_links)],
            3: [MessageHandler(Filters.text & ~Filters.command, get_need_link)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop),
                   CommandHandler('download_name', download_name)]
    )

    dp.add_handler(conv_handler_name)

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
