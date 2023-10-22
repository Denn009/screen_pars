import os
from pathlib import Path
from platform import system
from urllib.parse import urlparse
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

url = "https://proshoper.ru/actions/yarche/moskva/"

options = Options()
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

exec_path = os.path.join(os.getcwd(), 'driver', 'chromedriver.exe') if system() == "Windows" else \
    os.path.join(os.getcwd(), 'driver', 'chromedriver')

driver = webdriver.Chrome(options=options, service=Service(log_path=os.devnull, executable_path=exec_path))

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
  '''
})


def open_blocks(url, driver):
    driver.maximize_window()

    time.sleep(3)
    driver.close()
    driver.quit()


open_blocks(url, driver)