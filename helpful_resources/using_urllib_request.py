#!/usr/bin/env python3

import urllib.parse  # https://docs.python.org/3/library/urllib.parse.html
import urllib.request  # https://docs.python.org/3/library/urllib.request.html

url = "http://192.168.122.131/dvwa/login.php"

# Get
with urllib.request.urlopen(url) as response:
    content = response.read()
print(content)

# Post
data = {"username": "admin", "password": "password", "Login": "submit"}
data = urllib.parse.urlencode(data).encode()  # Data is now of type bytes
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
    content = response.read()
print(content)
