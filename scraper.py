import requests
import simplejson
from bs4 import BeautifulSoup
from data_parser import parse_table


def scrape_page(name, link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    content = soup.find("div", {"class": "mw-content-ltr"})

    tables = content.find_all("table", {"class": "wikitable", "style": "text-align: center; border-collapse: collapse; margin: 0em;"}, recursive=True)

    moves = list()

    for table in tables:
        moves.extend(parse_table(table))

    print(moves)

    with open('out/{name}.json'.format(name=name), 'w') as fp:
        fp.write(simplejson.dumps(moves, indent=4, sort_keys=False))

    return moves
