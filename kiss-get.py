#!/usr/bin/python

import unirest
from bs4 import BeautifulSoup

KISS_URI = "http://kissanime.com"

# Define the headers that will make us look like an iphone
unirest.default_header("User-Agent",
    "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/34.0.1847.18 Mobile/11B554a Safari/9537.53")
unirest.default_header("Accept", 
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
unirest.default_header("Accept-Language", "en-US,en;q=0.5")
unirest.default_header("Accept-Encoding", "gzip, deflate")
unirest.default_header("Accept-Language", "en-US,en;q=0.5")

# Get the home page of the mobile site
get_main = unirest.get(KISS_URI + "/M")

# Make a bootiful soop object
main_soup = BeautifulSoup(get_main.body)

series_map = dict()

# Get all the series on the main page
for series in main_soup.find_all('article'):
    series_div = series.find('div', class_='post-content')
    series_name = series_div.find('h2').get_text()
    series_link = series_div.find('a')['href']
    series_map[series_name] = KISS_URI + series_link


