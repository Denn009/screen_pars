from selenium import webdriver
import asyncio
import pyppeteer
from datetime import datetime


list_link = input("Введите ссылку на сайт или группу ссылок через пробел: ").split()
print("1: Фулскрин сайта")
print("2: Pass")
command = input("Введите команду: ")

# driver = webdriver.Chrome()
# driver.get("https://proshoper.ru/actions/yarche/moskva/")
# screenshot = driver.save_screenshot("first_screen.png")
# driver.quit()


async def full_screen(list_link):
    i = 1
    for link in list_link:
        browser = await pyppeteer.launch()
        page = await browser.newPage()
        await page.goto(link)
        tfn = datetime.now()
        time_for_name = f"{tfn.day}-{tfn.month}-{tfn.year}_{tfn.hour}:{tfn.minute}:{tfn.second}"
        await page.screenshot(path=f"full_screen_{time_for_name}_{i}.jpg", fullPage=True)
        await browser.close()
        print(f"Save full_screen_{i}.jpg")
        i += 1


if command == "1":
    asyncio.get_event_loop().run_until_complete(full_screen(list_link))
else:
    print('pass')