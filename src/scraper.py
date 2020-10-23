import requests
import simplejson
from bs4 import BeautifulSoup
from parser import parse_move_table
from pathlib import Path
from urllib.parse import urlparse


def scrape_game(game_name, pages):
    print(f"Processing {game_name} ...")

    characters = list()

    # Parse each character page
    for character_name, link in pages.items():
        characters.append(scrape_page(game_name, character_name, link))

    # Write to 'out' folder
    with open(f'out/{game_name}.json', 'w') as fp:
        fp.write(simplejson.dumps(characters, indent=4, sort_keys=False))

    print(f"finished.\n")


def scrape_page(game_name, character_name, link):
    print(f"  {character_name}...", end='')

    # Try to load page
    try:
        page = requests.get(link)
        domain = urlparse(link).scheme + "://" + urlparse(link).netloc
    except requests.RequestException:
        print(f"Unable to load page '{link}'")
        return

    output = dict()

    # Grab the tables from the page
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find("div", {"class": "mw-content-ltr"})

    # Parse character details
    character = soup.find("table", {"class": "wikitable"})\

    output["Name"] = character_name.replace('_', ' ')
    output["Game"] = game_name

    # Get Icon and Portrait image URLs
    images = soup.find_all("img", limit=5)
    output["IconURL"] = None
    try:
        output["PortraitURL"] = [domain + image["src"] for image in images if "portrait" in image["src"].lower()][0]
    except Exception:
        output["PortraitURL"] = None

    # TODO: Attributes
    output["Attributes"] = None

    # Parse each table for move(s)
    tables = content.find_all("table", {"class": "wikitable", "style": "text-align: center; border-radius: 4px; border: none; background-color: white; box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23); border-collapse: collapse; margin: 0em;"}, recursive=True)
    moves = list()
    for table in tables:
        moves.append(parse_move_table(table, domain))
    output["Moves"] = moves

    print(" done.")

    return output
