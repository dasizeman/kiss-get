#!/usr/bin/python

import shlex, subprocess
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

series_map = {}

# Get all the series on the main page
for series in main_soup.find_all('article'):
    series_div = series.find('div', class_='post-content')
    series_name = series_div.find('h2').get_text()
    series_link = series_div.find('a')['href']
    series_map[series_name] = KISS_URI + series_link

# TEST MODE: We will navigate to the first series
get_series = unirest.get(series_map[series_map.keys()[1]])

series_soup = BeautifulSoup(get_series.body)

episode_map = {}

for episode in series_soup.find_all('div', class_='episode'):
    episode_name = episode.get_text()
    episode_id = episode["data-value"]
    episode_map[episode_name] = episode_id

episode1_id = episode_map[episode_map.keys()[0]]
episode_post_uri = KISS_URI + "/Mobile/GetEpisode"

# This post uses AJAX magic to return episode links, so let's capture the response
vid_links_reponse = unirest.post(episode_post_uri, headers={"X-Requested-With":"XMLHttpRequest"}, params={"eID":episode1_id})

vid_link_soup = BeautifulSoup(vid_links_reponse.body)

vid_link_map = {}

for link in vid_link_soup.find_all('a'):
    vid_name = link.get_text()
    vid_link = link['href']
    vid_link_map[vid_name] = vid_link

# TEST MODE: Stream the 1080p one

# Build the command lines
curl_cmd = subprocess.Popen(shlex.split("curl -LX GET \"" + vid_link_map[vid_link_map.keys()[3]] + "\""), stdout=subprocess.PIPE)
mplayer_cmd = subprocess.Popen(shlex.split("mplayer -cache 16384 -"), stdin=curl_cmd.stdout)


