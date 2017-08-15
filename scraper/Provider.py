import requests
from Sources import slice_files
from bs4 import BeautifulSoup
import time
import zipfile
from io import BytesIO
import fnmatch
import csv 
from datetime import date

class SDR(object):
    def __init__(self, source_url):
        self.source_url = source_url

    def retrieve(self, date): #only do for one date
        """
            Returns the header and lines
        """
        date_str = date.strftime("%Y_%m_%d")

        r  = requests.get(self.source_url)
        soup = BeautifulSoup(r.text)
        
        found_file_for_date = False

        for link in soup.find_all('a'):
            if fnmatch.fnmatch(link.attrs['href'], '*{}*.zip'.format(date_str)):
                found_file_for_date = True

                request = requests.get(link.get('href'))
                zfile = zipfile.ZipFile(BytesIO(request.content))

                for name in zfile.namelist():
                        print("Pulling from: "+ name)
                        ex_file = zfile.open(name) # this is a file like object
                        content = ex_file.read().decode('utf-8') # now file-contents are a single string

                        lines = content.splitlines()

                        for i, line in enumerate(lines):
                            line = line.replace("\"", "")

                            if i == 0:
                                header = line
                                yield header, None
                            else:
                                yield None, line
            elif found_file_for_date is True:
                return
                    
if __name__ == "__main__":
    p = SDR("https://kgc0418-tdw-data2-0.s3.amazonaws.com/slices/GENERAL_COMMODITIES_SLICE.HTML")

    d = date(2017, 8, 12)

    for header, line in p.retrieve(d):
        if header is not None:
            print("Header:{}".format(header))
        else:
            print("Entry:{}".format(line))
    