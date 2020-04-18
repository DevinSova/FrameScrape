from pages import *
from scraper import scrape_page


def main():
    for character, link in DBFZ.items():
        scrape_page(character, link)
    for character, link in P4AU.items():
        scrape_page(character, link)
    for character, link in GBVS.items():
        scrape_page(character, link)


if __name__ == '__main__':
    main()
