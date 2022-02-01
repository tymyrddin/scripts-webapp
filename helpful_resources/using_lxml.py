#!/usr/bin/env python3

from io import BytesIO  # https://docs.python.org/3/library/io.html
from lxml import etree  # https://gregoryvigotorres.github.io/lxml_docs/index.html

import requests  # https://docs.python-requests.org/en/master/

url = "https://nostarch.com"

r = requests.get(url)  # Get
content = r.content  # Content is of type 'bytes'

parser = etree.HTMLParser()
# BytesIO: Use a byte string as a file object when parsing
content = etree.parse(BytesIO(content), parser=parser)  # Parse into tree
for link in content.findall("//a"):  # Find all "a" anchor elements.
    print(f"{link.get('href')} -> {link.text}")
