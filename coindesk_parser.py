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
    driver.set_page_load_timeout(10)
    try:
        driver.get(COINDESK_ADDR + "/latest-crypto-news")
    except selenium.common.exceptions.TimeoutException as e:
        #print(e)
        pass
    #print(BeautifulSoup(driver.page_source, "lxml"))
    for el in driver.find_elements(By.TAG_NAME, "button")[::-1]:
        if "More stories" in el.get_attribute("outerHTML"):
            btn = el
            break
    #print([el.get_attribute("outerHTML") for el in driver.find_elements(By.TAG_NAME, "button")])
    for i in range(NUM):
        driver.execute_script("arguments[0].click();", btn)
        for el in driver.find_elements(By.TAG_NAME, "button")[::-1]:
            if "More stories" in el.get_attribute("outerHTML"):
                btn = el
                break
        #driver.find_element(By.CSS_SELECTOR,
        #                    "bg-white hover:opacity-80 cursor-pointer border border-color-yellow-900 border-solid rounded-lg mb-8 text-color-charcoal-700 Noto_Sans_sm_Sans-600-sm py-1 px-4 h-10 flex items-center justify-center disabled:cursor-default").find_element(By.TAG_NAME, "button").click()
    soup = BeautifulSoup(driver.page_source, "lxml")
    # print(soup)
    hrefs = []
    for el in soup.find_all("div", { "class": "flex gap-4" }):
        hrefs.append(COINDESK_ADDR + el.find("a", { "class": "text-color-charcoal-900 mb-4 hover:underline" }, href=True)["href"])
    
    for h in hrefs:
        # if len(parsed) > 0 and h == list(parsed.keys())[0]: break
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