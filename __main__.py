from pages import P4AU
from data_parser import parse_moves_from_table
from scraper import scrape_page


def main():
    parse_moves_from_table(scrape_page(P4AU["Chie_Satonaka"]))


if __name__ == '__main__':
    main()
