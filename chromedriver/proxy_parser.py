import requests
from bs4 import BeautifulSoup
from user_agent import choice_user_agent


# Парсер proxy, который будет давать список с proxy, которые будут использованы в дальнейшем при парсинге
# На данный момент это просто заготовка, так как использовать ее пока негде
# https://best-proxies.ru/proxylist/free/ - сайт с proxy
def proxy_parser():
    # Заголовки запроса
    HEADERS = {
        'User-Agent': choice_user_agent(),
        'accept': '*/*',
        'path': '/f/AGSKWxX5DCelNV50_TQnazSCzoTHwq9hqhkgqu8JIi5x2DuieNPQ22VWtkYtsabsu0wtR4MfqvDn35ptlYQwqw7-c2MvgvS79vEV4UkSIAlfwJznXd--TRq_rF-K-lPYM7VGHwQm2ZjgfMY0x6nExhx8AowAzd0IQH-S-h4b-leLKOCoWoJQjvBRB6jAIIRT?fccs=W1siQUtzUm9sOHpRb1pwdHlndHhIWl93NVVzLVBSNy1DOGZvN0ptVDZXekNKdDFpRUJJRnpQdTFMa2RpWnM3ZVU1eUJiMUJ5VjdLQVd1czJ1NVVrdDRwb3FwSWRraW1UYTJjdWFJTE9PRTdBZW9JZ0FKMm13TjQ5SzRqeXI0aGJIZjRxUi1GUmc1TTBFMHVlUklVTjFpZ0ZSdFFmWjZWS28wTktBPT0iXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsWzE2NDc2ODUxMzgsMzgwMDAwMDBdLG51bGwsbnVsbCxudWxsLFtudWxsLFs3LDZdLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLDFdLCJodHRwczovL21hbmdhcG9pc2sucnUvbWFuZ2EvdmFucGFuY2htZW4vY2hhcHRlci8zMC0yMDIiLG51bGwsW11d'
    }

    content = requests.get(url="https://hidemy.name/ru/proxy-list/", headers=HEADERS).text
    soup = BeautifulSoup(content, "lxml")

    arr = soup.find("table").find_all("tr")
    proxy_list = []
    for item in arr[1:]:
        country = item.find("td").find_next().find_next().find("span", class_="country").text
        print(country)
        if country != "Russian Federation":
            proxy_list.append(f'{item.find("td").get_text()}:{item.find("td").find_next().get_text()}')

    for i in proxy_list:
        print(i)


if __name__ == "__main__":
    proxy_parser()
