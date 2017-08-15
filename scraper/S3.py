import boto
import boto.s3
import sys
from boto.s3.key import Key
import smart_open
import io
import csv
import os

#CREATE A FILE IN THIS DIRECTORY CALLED 'AWSKEY.py' and delcare two variables. e.g. 
"""
AWS_ACCESS_KEY_ID = 'AAAAAAAFTXXXGYBDHQXXX'
AWS_SECRET_ACCESS_KEY = 'AAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAA+WorrUgk'
"""
from AWSKey import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

bucket_name = 'sdr-repository'

CONN = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
BUCKET = CONN.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)

class SDRWriter(object):
    def setup(self, filename, local=True, is_eod=True):
        self._header_written = False
        self._is_file_open = False
        self.filename = filename
        self.local = local
        self.is_eod = is_eod

    def ___lazy_setup(self):
        if self.local:
            self.fout = open(self.filename, mode='wt')
        else:
            self.filename = "EOD/{}".format(self.filename) if self.is_eod and not self.filename.startswith("EOD/") else self.filename
            print("Setting Up to write {}".format(self.filename))
            self.fout = smart_open.smart_open('s3://{}:{}@sdr-repository/{}'.format(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, self.filename), 'wb')        
        
        self._is_file_open = True

    def exists(self, filename, local=True):
        if local:
            return os.path.isfile(filename) 
        else: 
            a = 'EOD/{}'.format(filename)
            return Key(BUCKET, a).exists()


    def write_header(self, line):
        if not self._is_file_open:
            self.___lazy_setup()

        self.write_row(line)
        self._header_written = True

    def is_header_written(self):
        return self._header_written

    def write_row(self, line):
        if not self._is_file_open:
            self.___lazy_setup()

        f = io.StringIO()
        f.write(line)
        f.write("\n")

        self.fout.write(f.getvalue())

    def teardown(self):
        if self._is_file_open:
            self.fout.close()

if __name__ == "__main__":
    import os
    print(os.getcwd())
    print("Testing upload")
    #SDRWriter().write("")
    aw = SDRWriter()
    aw.setup("test.csv", local=False)
    aw.write_row("adasdas")
    aw.teardown()