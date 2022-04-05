from seleniumwire import webdriver
import requests
from selenium.webdriver.common.by import By
import time
import random
from user_agent import choice_user_agent
import os


# Парср сайта mangalib
# При парсинге используется Selenium
# Есть минусы, которые нужно исправить, но это рабочий вариант
# Если не будет работать, то вот видео а
# получение страниц манги
def mangalib_parser(url):
    # опции для зпроса, если я правильно понял
    # Возможно, это аналог headers из requests
    options = webdriver.ChromeOptions()
    # передача в options user-agent
    options.add_argument(f"user-agent={choice_user_agent()}")

    # это нужно, так как нужен абсолютный путь к chromedriver.exe
    chromedriver_path = os.path.abspath("chromedriver.exe")
    driver = webdriver.Chrome(
        executable_path=chromedriver_path,
        options=options)

    url = url.split("=")

    try:
        options.add_argument(f"user-agent={choice_user_agent()}")
        driver.get(url="=".join(url))
        time.sleep(3)
        # получаем кол-во страниц в главе
        pages_count = int(driver.find_element(By.TAG_NAME, "option").get_attribute("text").split()[-1])
        pic_urls = []

        for page_num in range(1, pages_count + 1):
            print("ready")
            print("=".join([url[0], str(page_num)]))
            driver.get(url="=".join([url[0], str(page_num)]))
            time.sleep(random.randint(5, 10))
            array = list(map(lambda x: x.get_attribute("src"), driver.find_elements(By.TAG_NAME, "img")))
            pic_url = [i for i in array if i is not None][0]
            pic_urls.append(pic_url)

        page_number = 1
        title = url[0].split("/")[3]
        postfix = url[0].split("/")[4]
        os.mkdir(f"data\\manga\\{title}-{postfix}")
        for img_url in pic_urls:
            page = requests.get(img_url)
            # out = open(f"manga\\page-{page_number}.bmp", "wb")
            out = open(f"data\\manga\\{title}-{postfix}\\page-{page_number}.bmp", "wb")
            page_number += 1
            out.write(page.content)
            out.close()

        print("end")

    except Exception as e:
        print("Error")
        print(e)
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    mangalib_parser("https://mangalib.me/words-and-spirits/v1/c8?page=1")
