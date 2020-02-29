import requests
from bs4 import BeautifulSoup


def scrape_page(link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    content = soup.find("div", {"class": "mw-content-ltr"})

    moves = content.find_all("table", {"class": "wikitable", "style": "text-align: center; border-collapse: collapse; margin: 0em;"}, recursive=True)

    return moves

    # return soup.find("span", {"id": "Normal_Attacks"}).prettify()
