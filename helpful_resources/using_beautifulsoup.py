#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

url = "https://nostarch.com"

r = requests.get(url)  # Get
tree = BeautifulSoup(r.text, "html.parser")  # Parse into tree
for link in tree.find_all("a"):  # Find all "a" anchor elements.
    print(f"{link.get('href')} -> {link.text}")
