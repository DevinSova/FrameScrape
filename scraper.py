import requests
from bs4 import BeautifulSoup


def scrapePage(link):
    page = requests.get(link)

    soup = BeautifulSoup(page.content, 'html.parser')
