import requests
from bs4 import BeautifulSoup
import json
import os
import os.path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

FILENAME_DEF = "decrypt_news.json"

def DecryptParser(FILENAME):
    """
    Парсит новости с Decrypt.co
    Результат сохраняет в FILENAME
    Формат: json
    {
        [ссылка на страницу]: [ заголовок, дата, текст ]
    }
    Если ссылка уже присутствует в json, парсинг прекращается
    """
    DECRYPT_ADDR = "https://decrypt.co"
    with open(FILENAME, "r") as f: parsed = json.load(f)

    r = requests.get(DECRYPT_ADDR + "/news")
    soup = BeautifulSoup(r.text, "lxml")

    hrefs = []
    for el in soup.find_all("div", { "class": "mb-5 pb-5 last-of-type:mb-0" }):
        hrefs.append(DECRYPT_ADDR + el.find("a", { "class": "linkbox__overlay" },href=True)["href"])
        print(DECRYPT_ADDR + el.find("a", { "class": "linkbox__overlay" },href=True)["href"])
    
    with open(FILENAME, "w") as f: json.dump(parsed, f)

if __name__ == "__main__":
    if not os.path.exists(FILENAME_DEF):
        with open(FILENAME_DEF, "w") as f: f.write("{}")
    DecryptParser(FILENAME=FILENAME_DEF)