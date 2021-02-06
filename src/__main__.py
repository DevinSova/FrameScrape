from games import GAMES
from scraper import scrape_game

import sys


def main():
    if len(sys.argv) == 1:
        print("Usage: python3 __main__.py <GAME_NAME> <GAME_NAME>...")
        print("Games available: ", end='')
        for game_name, pages in GAMES.items():
            print(game_name, end=' ')
        print()
        exit(1)
    for arg in sys.argv[1:]:
        print(arg)
        scrape_game(arg, GAMES[arg])


if __name__ == '__main__':
    main()
