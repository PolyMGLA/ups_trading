import requests
from bs4 import BeautifulSoup
import json
import os
import os.path

FILENAME_DEF = "news.json"

def CoinDeskParser(FILENAME):
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

    r = requests.get(COINDESK_ADDR + "/latest-crypto-news")
    soup = BeautifulSoup(r.text, "lxml")

    hrefs = []
    for el in soup.find_all("div", { "class": "flex gap-4" }):
        hrefs.append(COINDESK_ADDR + el.find("a", { "class": "text-color-charcoal-900 mb-4 hover:underline" }, href=True)["href"])
    
    for h in hrefs:
        print("parsed:", h)
        if len(parsed) > 0 and h == list(parsed.keys())[0]: break
        req = requests.get(h)
        soup = BeautifulSoup(req.text, "lxml")
        section = soup.find("div", { "class": "pt-8 grid grid-cols-4 gap-2 md:grid-cols-8 md:gap-4 lg:grid-cols-12 xl:grid-cols-16 items-stretch" })
        caption = soup.find("h1", { "class": "text-headline-lg" }).getText()
        date = soup.find("div", { "class": "Noto_Sans_xs_Sans-400-xs flex gap-4 text-charcoal-600 flex-col md:flex-row" }).getText()
        text = ""
        for el in section.find_all("p"):
            text += el.getText() + "\n"
        parsed[h] = [caption, date, text]
    
    with open(FILENAME, "w") as f: json.dump(parsed, f)

if __name__ == "__main__":
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f: f.write("{}")
    CoinDeskParser(FILENAME=FILENAME_DEF)