import requests
from bs4 import BeautifulSoup
from user_agent import choice_user_agent, random_name_generation

HEADERS = {
        'User-Agent': choice_user_agent(),
        'accept': '*/*',
        'path': '/f/AGSKWxX5DCelNV50_TQnazSCzoTHwq9hqhkgqu8JIi5x2DuieNPQ22VWtkYtsabsu0wtR4MfqvDn35ptlYQwqw7-c2MvgvS79vEV4UkSIAlfwJznXd--TRq_rF-K-lPYM7VGHwQm2ZjgfMY0x6nExhx8AowAzd0IQH-S-h4b-leLKOCoWoJQjvBRB6jAIIRT?fccs=W1siQUtzUm9sOHpRb1pwdHlndHhIWl93NVVzLVBSNy1DOGZvN0ptVDZXekNKdDFpRUJJRnpQdTFMa2RpWnM3ZVU1eUJiMUJ5VjdLQVd1czJ1NVVrdDRwb3FwSWRraW1UYTJjdWFJTE9PRTdBZW9JZ0FKMm13TjQ5SzRqeXI0aGJIZjRxUi1GUmc1TTBFMHVlUklVTjFpZ0ZSdFFmWjZWS28wTktBPT0iXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsWzE2NDc2ODUxMzgsMzgwMDAwMDBdLG51bGwsbnVsbCxudWxsLFtudWxsLFs3LDZdLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLDFdLCJodHRwczovL21hbmdhcG9pc2sucnUvbWFuZ2EvdmFucGFuY2htZW4vY2hhcHRlci8zMC0yMDIiLG51bGwsW11d'
    }


# Получение html кода странциы
def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req.text


# считывание данных из файла с html кодом
def read_html():
    with open("code.html", "r", encoding="utf-8") as file:
        return file.read()


# запись html кода, делается это для того, чтобы не делать лишние запросы, а считывать html код из файла
def write_html(url):
    with open("code.html", "w", encoding="utf-8") as file:
        file.write(get_html(url))


# Парсер сайта https://tl.rulate.ru/
def rulate_parser(url):
    content = get_html(url)
    soup = BeautifulSoup(content, "lxml")

    text = soup.find("div", class_="content-text")
    file_name = random_name_generation()
    with open(f"data\\novel\\{file_name}", mode="w", encoding="utf-8") as file:
        for item in text:
            file.write(item.text + '\n')


if __name__ == "__main__":
    rulate_parser("https://tl.rulate.ru/book/70080/1870732/ready_new")
