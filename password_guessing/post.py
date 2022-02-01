#!/usr/bin/env python3

import requests  # https://docs.python-requests.org/en/master/


target_url = "http://192.168.122.131/dvwa/login.php"
data = {"username": "admin", "password": "password", "Login": "submit"}
response = requests.post(target_url, data=data)

print(response.content)
