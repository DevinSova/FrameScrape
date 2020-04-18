from games import GAMES
from scraper import scrape_game


def main():
    for game_name, pages in GAMES.items():
        scrape_game(game_name, pages)


if __name__ == '__main__':
    main()
