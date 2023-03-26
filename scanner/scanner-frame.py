#!/usr/bin/env python3

import re  # https://docs.python.org/3/library/re.html
import urllib.parse as urlparse  # https://docs.python.org/3/library/urllib.parse.html

import requests  # https://docs.python-requests.org/en/master/
from bs4 import BeautifulSoup  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/


class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links

    def extract_links_from(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

    def crawl(self, url=None):
        if url is None:
            url = self.target_url
        href_links = self.extract_links_from(url)
        for link in href_links:
            # Convert relative links
            link = urlparse.urljoin(url, link)
            # Strip # markup parts
            link = link.split("#")[0]
            # Only local links and make unique
            if (
                self.target_url in link
                and link not in self.target_links
                and link not in self.links_to_ignore
            ):
                self.target_links.append(link)
                print(link)
                self.crawl(link)

    def extract_forms(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content.decode(), features="lxml")
        return parsed_html.findAll("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        method = form.get("method")

        inputs_list = form.findAll("input")

        post_data = {}
        for form_input in inputs_list:
            input_name = form_input.get("name")
            input_type = form_input.get("type")
            input_value = form_input.get("value")
            if input_type == "text":
                input_value = value
            post_data[input_name] = input_value

        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for _form in forms:
                print("[+] Testing form in " + link)
                # ...
            if "=" in link:
                print("[+] Testing " + link)
                # ...
