import requests
from Sources import slice_files
from bs4 import BeautifulSoup
import time
import zipfile
from io import BytesIO
import fnmatch

if __name__ == "__main__":
    while(True):
        time.sleep(5)

        for url in slice_files():
            r  = requests.get(url)
            soup = BeautifulSoup(r.text)

            for link in soup.find_all('a'):
                request = requests.get(link.get('href'))
                zfile = zipfile.ZipFile(BytesIO(request.content))

                for name in zfile.namelist():
                    if fnmatch.fnmatch(name, '*.csv'):
                        ex_file = zfile.open(name) # this is a file like object
                        content = ex_file.read() # now file-contents are a single string
                        print(content)
                continue

            print("")