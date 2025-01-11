import requests
from bs4 import BeautifulSoup

def CoinDeskParser():
    COINDESK_ADDR = "https://www.coindesk.com"

    r = requests.get(COINDESK_ADDR + "/latest-crypto-news")
    soup = BeautifulSoup(r.text, "lxml")

    hrefs = []
    for el in soup.find_all("div", { "class": "flex gap-4" }):
        hrefs.append(COINDESK_ADDR + el.find("a", { "class": "text-color-charcoal-900 mb-4 hover:underline" }, href=True)["href"])
    
    lst = []
    for h in hrefs:
        req = requests.get(h)
        soup = BeautifulSoup(req.text, "lxml")
        section = soup.find("div", { "class": "pt-8 grid grid-cols-4 gap-2 md:grid-cols-8 md:gap-4 lg:grid-cols-12 xl:grid-cols-16 items-stretch" })
        caption = soup.find("h1", { "class": "text-headline-lg" }).getText()
        text = ""
        for el in section.find_all("p"):
            text += el.getText() + "\n"
        lst.append([ caption, text ])


    return lst

if __name__ == "__main__":
    print(CoinDeskParser()[0])