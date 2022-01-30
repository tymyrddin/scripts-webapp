#!/usr/bin/env python3

from bs4 import BeautifulSoup  # https://docs.python-requests.org/en/master/

import requests  # https://docs.python-requests.org/en/master/
import urllib.parse as urlparse  # https://docs.python.org/3/library/urllib.parse.html


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "http://192.168.122.131/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)
parsed_html = BeautifulSoup(str(response.content), features="lxml")
forms_list = parsed_html.findAll("form")

for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    method = form.get("method")
    enctype = form.get("enctype")
    form_id = form.get("id")

    inputs_list = form.findAll("input")

    post_data = {}
    for form_input in inputs_list:
        input_name = form_input.get("name")
        input_type = form_input.get("type")
        input_value = form_input.get("value")
        if input_type == "text":
            input_value = "test"
        post_data[input_name] = input_value

    result = requests.post(post_url, data=post_data)
    print(result.content.decode())
