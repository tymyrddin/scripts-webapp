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
            # Strip # markup
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
        parsed_html = BeautifulSoup(str(response.content), features="lxml")
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
            for form in forms:
                print("\n[+] Testing form in " + link)
                is_vulnerable_to_xss = self.test_xss_in_form(form, link)
                if is_vulnerable_to_xss:
                    print("[***] XSS vuln found in link " + link + "in the form")
                    print(form)

            if "=" in link:
                print("\n[+] Testing " + link)
                is_vulnerable_to_xss = self.test_xss_in_link(link)
                if is_vulnerable_to_xss:
                    print("[***] XSS vuln found in link " + link)

    def test_xss_in_link(self, url):
        xss_test_script = "<sCript>alert('test')</scriPt>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script.encode() in response.content

    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>alert('test')</scriPt>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script.encode() in response.content
