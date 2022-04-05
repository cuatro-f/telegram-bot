# Найди бота здесь
# t.me/dup_durup_dup_bot

import logging
import telegram
from telegram.ext import Updater, MessageHandler, Filters

from mangalib_parser import mangalib_parser
from mangapoisk_parser import parser_mangapoisk
from proxy_parser import get_one_proxy

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5237678741:AAG9O-IJYkAH3TRlVqqyM5Td2sKWNwP6tsA'


# для прокси - не работает
REQUEST_KWARGS = {
    # 'proxy_url': 'socks5://ip:port', # Адрес прокси сервера
    'proxy_url': get_one_proxy(), # Адрес прокси сервера
    # Опционально, если требуется аутентификация:
    # 'urllib3_proxy_kwargs': {
    #     'assert_hostname': 'False',
    #     'cert_reqs': 'CERT_NONE'
    #     'username': 'user',
    #     'password': 'password'
    # }
}


def download_manga(update, context):
    url = update.message.text
    update.message.reply_text('Идет скачиваение...')
    # mangalib_parser(url)
    print(url)
    # url = 'https://mangapoisk.ru/manga/berserk/chapter/26-240'
    parser_mangapoisk(url)
    update.message.reply_text('Готово')


def main():
    # Создаём объект updater.

    # вкл если хочешь работать без прокси
    updater = Updater(TOKEN)

    # влк если хочешь работать с прокси (только выкл предыдущее)
    # ШТУКА ДЛЯ ПРОКСИ ОТСЮДА

    # good_proxy = False
    # while not good_proxy:
    #     try:
    #         updater = Updater(TOKEN, use_context=True,
    #                           request_kwargs=REQUEST_KWARGS)
    #         good_proxy = True
    #     except telegram.error.NetworkError:
    #         pass

    # ДОСЮДА

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, download_manga)

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()