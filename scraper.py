import requests
from bs4 import BeautifulSoup


def scrape_page(link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    moves = soup.find_all("table", {"class": "wikitable"})
    return moves[1]

    for move in moves:
        return move
        # for field in move.find_all("a"):
        #     print(field.contents)

    # return soup.find("span", {"id": "Normal_Attacks"}).prettify()
