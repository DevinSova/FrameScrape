from pages import P4AU
from data_parser import parse_moves
from scraper import scrape_page


def main():
    parse_moves(scrape_page(P4AU["Chie_Satonaka"]))


if __name__ == '__main__':
    main()
