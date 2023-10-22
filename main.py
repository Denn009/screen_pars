import os
from pathlib import Path
from platform import system
from urllib.parse import urlparse
from datetime import datetime
import time
from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

list_url = input("Введите ссылку на сайт || Или группу ссылок через пробел: ").split()
print("==============")
print("1 - Построчно нарезанное изображение")
print("2 - Фуллскрин всего сайта")
print("==============")
command = int(input("Введите номер команды: "))
time_for_sleep = input("Введите задержку в секундах: ")

if not time_for_sleep.isdigit():
    time_for_sleep = 0
else:
    time_for_sleep = int(time_for_sleep)

if command == 1:
    print("-------")
    print("По умолчанию: 1530 - 6 строк товаров")
    crop_height = input("Введите высоту нарезаемых изображений: ")

    if not crop_height.isdigit():
        crop_height = 1530
    else:
        crop_height = int(crop_height)

    # print("-------")
    # print("По умолчанию: Нет")
    # with_head = input("С заголовком? Да/Нет: ")
    # if with_head.lower() == "да":
    #     with_head = True
    # else:
    #     with_head = False


print("Выполняется...")


def get_time():
    time_now = datetime.now()
    return f"{time_now.day}-{time_now.month}-{time_now.year}_{time_now.hour}-{time_now.minute}-{time_now.second}"


def open_block(driver):
    element_list = driver.find_elements(By.CSS_SELECTOR, "div.products_show_more")

    if len(element_list) > 0:

        actions = ActionChains(driver)

        for fe in element_list:
            actions.move_to_element(fe).perform()
            fe.click()

        header = driver.find_element(By.CSS_SELECTOR, "header.block__header")
        actions.move_to_element(header).perform()
        time.sleep(3)


def get_full_screen(url):
    if not os.path.exists("full_screen"):
        os.makedirs("full_screen")

    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    open_block()

    i = 1
    time_now = get_time()
    path = "full_screen/fullscreen_" + time_now + "_" + str(i) + ".png"
    time.sleep(time_for_sleep)
    s = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
    driver.set_window_size(s('Width'), s('Height'))
    driver.find_element(By.TAG_NAME, 'body').screenshot(path)
    driver.close()
    driver.quit()


def get_screen(url, crop_height, with_head):
    if not os.path.exists("screen"):
        os.makedirs("screen")

    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })

    driver.get(url)
    open_block(driver)
    i = 1

    element_list = driver.find_elements(By.XPATH, '//section[@class="md:flex md:flex-wrap"]')
    actions = ActionChains(driver)

    for elem in element_list:
        time_now = get_time()
        path = "screen_" + time_now + "_" + str(i) + ".png"
        actions.move_to_element(elem).perform()
        time.sleep(time_for_sleep)
        s = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
        driver.set_window_size(s('Width'), s('Height'))
        time.sleep(time_for_sleep)
        elem.screenshot("screen/" + path)
        print("---------------")
        print(f"Сохраняется скриншот {i}")

        cut_img(path, crop_height, with_head)
        i += 1
        time.sleep(time_for_sleep)

    driver.close()
    driver.quit()


def cut_img(path, crop_height, with_head):
    if not os.path.exists("corp_screen"):
        os.makedirs("corp_screen")

    with Image.open("screen/" + path) as img:
        width, height = img.size
        count_row = height // crop_height
        y1 = 36

        for i in range(1, count_row + 1):
            y2 = crop_height * i
            img_crop = img.crop((0, y1, width, y2))
            y1 = y2
            new_path = "corp_screen/corp" + str(i) + "_" + path
            img_crop.save(new_path)

        img_crop = img.crop((0, y1, width, height))
        img_crop.save("corp_screen/corp-last_" + path)


def control(list_url, command, crop_height,with_head):
    if command == 1:
        for url in list_url:
            get_screen(url, crop_height, with_head)
            time.sleep(4)

    elif command == 2:
        for url in list_url:
            get_full_screen(url)
            time.sleep(4)

    else:
        print("Неизвестная команда")


control(list_url, command, crop_height, with_head=False)
