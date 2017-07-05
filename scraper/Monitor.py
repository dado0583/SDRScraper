import requests
from Sources import slice_files
from bs4 import BeautifulSoup
import time

if __name__ == "__main__":
    while(True):
        time.sleep(5)

        for url in slice_files():
            r  = requests.get(url)
            soup = BeautifulSoup(r.text)

            for link in soup.find_all('a'):
                print(link.get('href'))

            print("")