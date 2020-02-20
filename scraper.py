import requests
from bs4 import BeautifulSoup


def scrapePage(link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    moves = soup.find_all("table", {"class": "wikitable"})
    for move in moves:
        print(move)
        # for field in move.find_all("a"):
        #     print(field.contents)

    # return soup.find("span", {"id": "Normal_Attacks"}).prettify()
