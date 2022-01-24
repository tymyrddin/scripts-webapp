#!/usr/bin/env python3

import requests         # https://docs.python-requests.org/en/master/

target_url = "google.com"


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


with open("subdomain.list", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
            print("[+] Discovered subdomain: " + test_url)
