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

class DecryptRealTimeParser(Thread):
    """
    Потоковый парсер новостей с Decrypt
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
        DECRYPT_ADDR = "https://decrypt.co"
        r = requests.get(DECRYPT_ADDR + "/news")
        soup = BeautifulSoup(r.text, "lxml")
        url = DECRYPT_ADDR \
            + soup.find("div", { "class": "flex flex-col border-l-[0.5px] ml-0.5 border-neutral-300 pl-2 md:pl-3 xl:pl-4 pt-7" }) \
            .find("a",
                  { "class": "linkbox__overlay" },
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
            section = soup.find("div", { "class": "z-2 flex-1 min-w-0" })
            caption = section.find("h1").getText()
            date = soup.find("span", { "class": "font-akzidenz-grotesk scene:font-itc-avant-garde-gothic-pro scene:font-light font-normal text-sm/4.5 md:text-base/5 xl:text-lg/5 scene:text-sm whitespace-nowrap" }).find("time").getText()
            text = ""
            for el in section.find_all("p"):
                if el == None: continue
                text += el.getText() + "\n"
            return { h: [caption, date, text] }
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
    thread = DecryptRealTimeParser()
    thread.start()