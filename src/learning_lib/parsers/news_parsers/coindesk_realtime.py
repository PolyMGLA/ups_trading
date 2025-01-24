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

from threading import Thread

N_CORES = 12

class CoinDeskRealTimeParser(Thread):
    """
    Потоковый парсер новостей с CoinDesk
    """
    last_url = None
    running = True
    parsed = { }

    def run(self):
        while self.running:
            url = self.get_page_last_url()
            if self.last_url != url:
                print("parsing:", url)
                self.last_url = url
                v = self.parse_url(url)
                self.parsed = { **self.parsed, **v }
            time.sleep(10)
    
    def get_page_last_url(self) -> str:
        """
        Получить ссылку на последнюю запись
        :returns: url последней новости
        """
        COINDESK_ADDR = "https://www.coindesk.com"
        r = requests.get(COINDESK_ADDR + "/latest-crypto-news")
        soup = BeautifulSoup(r.text, "lxml")
        url = COINDESK_ADDR \
            + soup.find("div", { "class": "flex gap-4" }) \
            .find("a",
                  { "class": "text-color-charcoal-900 mb-4 hover:underline" },
                  href=True
            )["href"]
        return url

    @staticmethod
    def parse_url(h):
        """
        Прочитать информацию со страницы
        :param h: url требуемой страницы
        """
        try:
            req = requests.get(h)
            soup = BeautifulSoup(req.text, "lxml")
            section = soup.find("div", { "class": "pt-8 grid grid-cols-4 gap-2 md:grid-cols-8 md:gap-4 lg:grid-cols-12 xl:grid-cols-16 items-stretch" })
            caption = soup.find("h1", { "class": "text-headline-lg" }).getText()
            date = soup.find("div", { "class": "Noto_Sans_xs_Sans-400-xs flex gap-4 text-charcoal-600 flex-col md:block" }).getText()
            tm = time.strftime("%H:%M",
                            time.strptime(
                                date[date.find(":") - 2:date.find(":") + 5]
                                .replace("p", "PM").replace("a", "AM").strip(), "%I:%M\u202f%p"))
            if "Published" in date:
                date = date[date.find("Published") + 9:]
            date = date.replace("Updated", "")[1:13].replace(",", "")
            text = ""
            for el in section.find_all("p"):
                if el is None: continue
                text += el.getText() + "\n"
            return { h: [caption, date + " " + tm, text] }
        except Exception as e:
            print(e)
            return { }

    def fetch_n_clear(self) -> dict[str, list[str]]:
        """
        Очищает и возвращает накопленные данные
        :returns: словарь { href: [caption, date, text] }
        """
        p = self.parsed.copy()
        self.parsed = { }
        return p

    def stop(self, timeout=.0) -> None:
        """
        Останавливает выполнение потока
        :param timeout: таймаут завершения, по умолчанию 0. Нет смысла указывать точность больше,
        чем 10 с, так как проверка проводится раз в 10 секунд
        """
        time.sleep(timeout)
        self.running = False

    def _import(self, FILENAME) -> None:
        """
        Импортирует данные из файла в формате json в словарь
        :param FILENAME: имя входного файла
        """
        if not os.path.exists(FILENAME):
            print("file not found, creating..")
            with open(FILENAME, "w") as f: f.write("{}")
        with open(FILENAME, "r") as f:
            data = json.load(f)
        data = dict(reversed(data.items()))
        self.parsed = { **self.parsed, **data }

    def _export(self, FILENAME) -> None:
        """
        Экспортирует накопленные данные в файл в формате json
        :param FILENAME: имя выходного файла. Если он не существует, будет создан
        """
        if not os.path.exists(FILENAME):
            print("file not found, creating..")
            with open(FILENAME, "w") as f: f.write("{}")
        with open(FILENAME, "w") as f:
            json.dump(
                dict(reversed(self.parsed.items())),
                f,
                indent=4)

if __name__ == "__main__":
    thread = CoinDeskRealTimeParser()
    thread.start()