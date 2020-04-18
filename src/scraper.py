import requests
import simplejson
from bs4 import BeautifulSoup
from data_parser import parse_table
from pathlib import Path


def scrape_game(game_name, pages):
    print(f"Processing {game_name} ...")
    for character_name, link in pages.items():
        scrape_page(game_name, character_name, link)
    print(f"{game_name} done.")


def scrape_page(game_name, character_name, link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')

    content = soup.find("div", {"class": "mw-content-ltr"})

    tables = content.find_all("table", {"class": "wikitable", "style": "text-align: center; border-collapse: collapse; margin: 0em;"}, recursive=True)

    moves = list()

    print(f"  {character_name}...", end='')

    for table in tables:
        moves.extend(parse_table(table))

    Path(Path.cwd(), f'out/{game_name}/').mkdir(parents=True, exist_ok=True)

    with open(f'out/{game_name}/{character_name}.json', 'w') as fp:
        fp.write(simplejson.dumps(moves, indent=4, sort_keys=False))

    print(" done.")
