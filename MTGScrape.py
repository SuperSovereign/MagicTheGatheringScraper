import requests, os, bs4, lxml, re
from urllib.parse import urlparse, urljoin

format1 = "Modern"
archtype = "grixis-delver"

# url of deck archtype
site = "https://mtgdecks.net"
url = site + "/" + format1 + "/" + archtype

def is_absolute(url):
        """
        Check if a hyperlink is absolute or relative
        """
        return bool(urlparse(url).netloc)

def rel_fix(base_link, url):
    if not is_absolute(url):
                        return urljoin(base_link,url)
    else:
                        return url
		


print(url)
outside_list = []


def recursive_search(current_url):
    current_url = rel_fix(current_url,url)
    response_text = requests.get(current_url).text
    outside_list.append(response_text)
    soup = bs4.BeautifulSoup(response_text,"lxml") 
    all_tags = soup.findAll("a",href=True,text=["Grixis Delver","Grixis Death Shadow","Grixis Shadow","Grixis Aggro","4c Death's Shadow"])
    all_links = [tag['href'] for tag in all_tags]
    for link in all_links:
        print(link)
        link2 = site + link + "/txt"
        print(link2)
        response_deck = requests.get(link2).text
        #print(response_deck)
        
        f = open("/Users/brianjones/Documents/Decks%s" % link, "a+")
        f.write(response_deck)
        f.close()
        
        
recursive_search(url)
print('Done.')
