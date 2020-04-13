from pages import P4AU, DBFZ
from scraper import scrape_page


def main():
    for character, link in P4AU.items():
        scrape_page(character, link)


if __name__ == '__main__':
    main()
