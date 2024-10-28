import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import Firefox
from typing import List, Dict, Optional

URL: str = "https://github.com/AcademySoftwareFoundation/MaterialX"
page = requests.get(URL)


def get_page(url: str = URL) -> str:
    # get the raw html from input page
    assert url
    return requests.get(url).text


if __name__ == "__main__":
    print(page.text)
