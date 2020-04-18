from pages import GAMES
from scraper import scrape_game


def main():
    scrape_game("P4AU", GAMES["P4AU"])


if __name__ == '__main__':
    main()
