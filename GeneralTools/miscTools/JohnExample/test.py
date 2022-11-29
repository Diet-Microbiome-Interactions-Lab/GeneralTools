import argparse
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
import datetime as dt


class JohnnyCash:

    def __init__(self, username, password, login_url, data_url):
        self.username = username
        self.password = password
        self.login_url = login_url
        self.data_url = data_url

    def firstPart(self):
        page = s.get(data_url, headers={
                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'})


def parse_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-1", "--In1", help="One of two files to compare to one another",
                        required=True)
    parser.add_argument("-2", "--In2", help="One of two files to compare to one another",
                        required=True)
    parser.add_argument("-o", "--Output", help="Output file name",
                        required=True, default="")
    return parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    main(args)
