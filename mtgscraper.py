#! /usr/bin/env python3
#MTG Scrape
import requests, bs4, lxml, re
from pathlib import Path
from urllib.parse import urlparse, urljoin

MTGDECKS_URL = "https://mtgdecks.net"
decks_dir = Path.home() /'Documents' / 'deck'

def recursive_search_format(format_url):
    response_text = requests.get(format_url).text
    soup = bs4.BeautifulSoup(response_text,"lxml")
    table_f = soup.find("table", id="archetypesTable")
    all_tags_f = table_f.findAll("a")
    all_links_f = [tag['href'] for tag in all_tags_f]

    for link_f in all_links_f:
        print(link_f)
        urld = MTGDECKS_URL + link_f
        deck_name = link_f.split('/')[-1]

        response_text = requests.get(urld).text
        soup = bs4.BeautifulSoup(response_text,"lxml")
        all_tags = soup.select("td > a:nth-of-type(1)")
        all_links = [tag['href'] for tag in all_tags]
        set_links = set(all_links)

        for link in set_links:
            #print(link)
            deck_variant = link.split('/')[-1]
            link2 = MTGDECKS_URL + link + "/txt"
            response_deck = requests.get(link2).text

            deck_dir = decks_dir / deck_format / deck_name
            deck_dir.mkdir(parents=True, exist_ok=True)

            deckfile = deck_dir / (deck_variant +'.txt')
            if not deckfile.is_file():
                print(deckfile)
                with deckfile.open('a+') as f:
                    f.write(response_deck)

format_list = ["Standard", "Modern", "Legacy", "Vintage", "Pauper"]
for deck_format in format_list:
    url = MTGDECKS_URL + "/" + deck_format
    recursive_search_format(url)
print('Done.')
