#!/usr/bin/python
"""
Script to create user accounts given CSV
"""

import csv
import sys
import requests
__URL__ = "http://10.102.56.95:8080/accounts/api/register/"


def create_accounts(file_location):
    reader = csv.DictReader(open(file_location, 'rb'), delimiter='\t')
    for record in reader:
        data = {'first_name': record['firstname'],
                'last_name': record['lastname'],
                'username': record['email'],
                'email': record['email'],
                'password': '123123',
                'remoteid': record['remotecentername'],
                'mobile': record['mobile'],
                'city': record['city'],
                'remotecentrename': record['remotecentername']
                }
        req = requests.post(__URL__, data=data)
        if req.status_code!=201 or req.status_code!=200:
            print "ERROR processing record", record
            print req.text
            sys.exit(1)


if __name__ == "__main__":
    create_accounts(sys.argv[1])
