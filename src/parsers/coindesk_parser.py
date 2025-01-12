import requests
from bs4 import BeautifulSoup
import json
import os
import os.path
import tqdm
import time

from joblib import Parallel, delayed

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

FILENAME_DEF = "coindesk_news.json"
NUM_DEF = 4
N_CORES = 4

def parse_url(h):
    try:
        global parsed
        if h in parsed:
            # print("skipping:", h)
            return { }
        time.sleep(.25)
        req = requests.get(h)
        soup = BeautifulSoup(req.text, "lxml")
        section = soup.find("div", { "class": "pt-8 grid grid-cols-4 gap-2 md:grid-cols-8 md:gap-4 lg:grid-cols-12 xl:grid-cols-16 items-stretch" })
        caption = soup.find("h1", { "class": "text-headline-lg" }).getText()
        date = soup.find("div", { "class": "Noto_Sans_xs_Sans-400-xs flex gap-4 text-charcoal-600 flex-col md:flex-row" }).getText()
        tm = time.strftime("%H:%M",
                        time.strptime(
                            date[date.find(":") - 2:date.find(":") + 5]
                            .replace("p", "PM").replace("a", "AM").strip(), "%I:%M\u202f%p"))

        # print(tm)
        date = date.replace("Updated", "")[1:13].replace(",", "")
        text = ""
        for el in section.find_all("p"):
            if el == None: continue
            text += el.getText() + "\n"
        parsed[h] = [caption, date, text]
        return { h: [caption, date + " " + tm, text] }
    except Exception as e:
        print(e)
        return { }


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
    global parsed
    with open(FILENAME, "r") as f: p = json.load(f)
    parsed = { }
    for el in p:
        if el == { }: continue
        parsed[el] = p[el]
    # print(parsed)

    #r = requests.get(COINDESK_ADDR + "/latest-crypto-news")
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(10)
    try:
        driver.get(COINDESK_ADDR + "/latest-crypto-news")
    except selenium.common.exceptions.TimeoutException as e:
        pass
    btn = None
    for el in driver.find_elements(By.TAG_NAME, "button")[::-1]:
        if "More stories" in el.get_attribute("outerHTML"):
            btn = el
            break
    # print("press q to break")
    try:
        for i in tqdm.tqdm(range(NUM)):
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(.65)
    except Exception as e:
        print(e)
    
    # print("interrupted on i =", i)
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.close()
    hrefs = []
    for el in soup.find_all("div", { "class": "flex gap-4" }):
        hrefs.append(COINDESK_ADDR + el.find("a", { "class": "text-color-charcoal-900 mb-4 hover:underline" }, href=True)["href"])
    print("parsing..")
    
    data = Parallel(n_jobs=N_CORES, verbose=10)(delayed(parse_url)(h) for h in tqdm.tqdm(hrefs))
    # print(data)
    for el in data:
        if el == { }: continue
        # print(el)
        parsed[list(el.keys())[0]] = list(el.values())[0]
    with open(FILENAME, "w") as f: json.dump(parsed, f, indent=4)

if __name__ == "__main__":
    if not os.path.exists(FILENAME_DEF):
        with open(FILENAME_DEF, "w") as f: f.write("{}")
    CoinDeskParser(FILENAME=FILENAME_DEF, NUM=NUM_DEF)