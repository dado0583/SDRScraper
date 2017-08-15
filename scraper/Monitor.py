import requests
from Sources import slice_files
from bs4 import BeautifulSoup
import time
import zipfile
from io import BytesIO
import fnmatch
import csv 
from Provider import SDR
from datetime import date, timedelta
import S3

def dates(end_date):
    d = end_date
    delta = timedelta(days=1)
    while d <= end_date:
        yield d
        d -= delta

if __name__ == "__main__":
        IS_LOCAL = False
    #while(True):
        srcs = slice_files()
        for asset_class in srcs:
            url = srcs[asset_class]

            starting_date = date.today()

            for d in dates(starting_date):
                if (starting_date-d).days > 10:
                    break #Covers the case where we haven't run this for 10 days.

                s3 = S3.SDRWriter()

                filename = "{}_{}.csv".format(asset_class, d.strftime("%Y_%m_%d"))

                if "CUMULATIVE" in url and s3.exists(filename, local=IS_LOCAL):
                    print("Skipping {} because it already exists".format(filename))
                    continue

                s3.setup(filename, local=IS_LOCAL)

                sdr = SDR(url)

                for header, line in sdr.retrieve(d):
                    if header is not None and not s3.is_header_written():
                        #print("Header:{}".format(header))
                        s3.write_header(header)
                    elif line is not None:
                        #print("Entry:{}".format(line))
                        s3.write_row(line)

                s3.teardown()
    