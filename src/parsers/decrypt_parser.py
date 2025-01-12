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

FILENAME_DEF = "decrypt_news.json"
NUM_DEF = 4
N_CORES = 12

def parse_url(h):
    try:
        global parsed
        if h in parsed:
            # print("skipping:", h)
            return { }
        # print(h)
        time.sleep(.25)
        req = requests.get(h)
        soup = BeautifulSoup(req.text, "lxml")
        # print(soup.find_all("h1"))
        section = soup.find("div", { "class": "z-2 flex-1 min-w-0" })
        caption = section.find("h1").getText()
        date = soup.find("span", { "class": "font-akzidenz-grotesk scene:font-itc-avant-garde-gothic-pro scene:font-light font-normal text-sm/4.5 md:text-base/5 xl:text-lg/5 scene:text-sm whitespace-nowrap" }).find("time").getText()
        #date = date.replace("Updated", "")[1:13].replace(",", "")
        text = ""
        for el in section.find_all("p"):
            if el == None: continue
            text += el.getText() + "\n"
        parsed[h] = [caption, date, text]
        return { h: [caption, date, text] }
    except Exception as e:
        print(e)
        return { }


def DecryptParser(FILENAME, NUM):
    """
    Парсит новости с Decrypt.so
    Результат сохраняет в FILENAME
    Формат: json
    {
        [ссылка на страницу]: [ заголовок, дата, текст ]
    }
    Если ссылка уже присутствует в json, парсинг прекращается
    """
    COINDESK_ADDR = "https://decrypt.co"
    global parsed
    with open(FILENAME, "r") as f: p = json.load(f)
    parsed = { }
    for el in p:
        if el == { }: continue
        parsed[el] = p[el]
    # print(parsed)

    #r = requests.get(COINDESK_ADDR + "/latest-crypto-news")
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(30)
    try:
        driver.get(COINDESK_ADDR + "/news")
    except selenium.common.exceptions.TimeoutException as e:
        pass
    btn = None
    for el in driver.find_elements(By.TAG_NAME, "button")[::-1]:
        if "Load More" in el.get_attribute("outerHTML"):
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
    for el in soup.find_all("div", { "class": "flex flex-col border-l-[0.5px] ml-0.5 border-neutral-300 pl-2 md:pl-3 xl:pl-4 pt-7" }):
        # print(el)
        # print(el.find("a", { "class": "linkbox__overlay" }, href=True))
        hrefs.append(COINDESK_ADDR + el.find("a", { "class": "linkbox__overlay" }, href=True)["href"])
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
    DecryptParser(FILENAME=FILENAME_DEF, NUM=NUM_DEF)