#!/usr/bin/env python3

import requests  # https://docs.python-requests.org/en/master/

url = "http://192.168.122.131/dvwa/login.php"

# Get
response = requests.get(url)
# response.text = string; response.content = bytestring
print(response.content)

# Post
data = {"username": "admin", "password": "password", "Login": "submit"}
response = requests.post(url, data=data)
# response.text = string; response.content = bytestring
print(response.content)
