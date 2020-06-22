import requests
import simplejson
from bs4 import BeautifulSoup
from data_parser import parse_move_table
from pathlib import Path
from urllib.parse import urlparse


def scrape_game(game_name, pages):
    print(f"Processing {game_name} ...")

    # Parse each character page
    for character_name, link in pages.items():
        scrape_page(game_name, character_name, link)

    print(f"finished.\n")


def scrape_page(game_name, character_name, link):
    print(f"  {character_name}...", end='')

    # Try to load page
    try:
        page = requests.get(link)
    except requests.RequestException:
        print(f"Unable to load page '{link}'")
        return

    output = dict()

    # Grab the tables from the page
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find("div", {"class": "mw-content-ltr"})

    # Parse character details
    character = soup.find("table", {"class": "wikitable"})
    sections = character.find_all("tr")
    output["Name"] = sections[0].find("th").text.replace('\n', '')
    output["Game"] = game_name
    try:
        output["ImageURL"] = urlparse(link).netloc + sections[1].find("a")["href"]
    except Exception:
        output["ImageURL"] = ""

    try:
        output["Attributes"] = sections[2].text
    except Exception:
        output["Attributes"] = ""

    # Parse each table for move(s)
    tables = content.find_all("table", {"class": "wikitable", "style": "text-align: center; border-collapse: collapse; margin: 0em;"}, recursive=True)
    moves = list()
    for table in tables:
        moves.append(parse_move_table(table))
    output["Moves"] = moves

    # Write to 'out' folder
    Path(Path.cwd(), f'out/{game_name}/').mkdir(parents=True, exist_ok=True)
    with open(f'out/{game_name}/{character_name}.json', 'w') as fp:
        fp.write(simplejson.dumps(output, indent=4, sort_keys=False))

    print(" done.")
