import requests
from bs4 import BeautifulSoup
import json
import os
import os.path

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

FILENAME_DEF = "coindesk_news.json"
NUM_DEF = 1000

def CoinDeskParser(FILENAME, NUM):
    """
    Парсит новости с CoinDesk
    Результат сохраняет в FILENAME
    Формат: json
    {
        [ссылка на страницу]: [ заголовок, дата, текст ]
    }
    Если ссылка уже присутствует в json, парсинг прекращается
    """
    COINDESK_ADDR = "https://www.coindesk.com"
    with open(FILENAME, "r") as f: parsed = json.load(f)

    #r = requests.get(COINDESK_ADDR + "/latest-crypto-news")
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(1)
    try:
        driver.get(COINDESK_ADDR + "/latest-crypto-news")
    except selenium.common.exceptions.TimeoutException as e:
        pass
    for el in driver.find_elements(By.TAG_NAME, "button")[::-1]:
        if "More stories" in el.get_attribute("outerHTML"):
            btn = el
            break
    for i in range(NUM):
        driver.execute_script("arguments[0].click();", btn)
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.close()
    hrefs = []
    for el in soup.find_all("div", { "class": "flex gap-4" }):
        hrefs.append(COINDESK_ADDR + el.find("a", { "class": "text-color-charcoal-900 mb-4 hover:underline" }, href=True)["href"])
    
    for h in hrefs:
        if h in parsed: 
            print("saved:", h)
            continue
        print("parsing:", h)
        req = requests.get(h)
        soup = BeautifulSoup(req.text, "lxml")
        section = soup.find("div", { "class": "pt-8 grid grid-cols-4 gap-2 md:grid-cols-8 md:gap-4 lg:grid-cols-12 xl:grid-cols-16 items-stretch" })
        caption = soup.find("h1", { "class": "text-headline-lg" }).getText()
        date = soup.find("div", { "class": "Noto_Sans_xs_Sans-400-xs flex gap-4 text-charcoal-600 flex-col md:flex-row" }).getText()
        text = ""
        for el in section.find_all("p"):
            text += el.getText() + "\n"
        parsed[h] = [caption, date, text]
    
    with open(FILENAME, "w") as f: json.dump(parsed, f, indent=4)

if __name__ == "__main__":
    if not os.path.exists(FILENAME_DEF):
        with open(FILENAME_DEF, "w") as f: f.write("{}")
    CoinDeskParser(FILENAME=FILENAME_DEF, NUM=NUM_DEF)