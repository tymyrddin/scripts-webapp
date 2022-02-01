#!/usr/bin/env python3

import argparse  # https://docs.python.org/3/library/argparse.html
import re  # https://docs.python.org/3/library/re.html
import requests  # https://docs.python-requests.org/en/master/
import textwrap  # https://docs.python.org/3/library/textwrap.html
import urllib.parse as urlparse  # https://docs.python.org/3/library/urllib.parse.html


def get_args():
    parser = argparse.ArgumentParser(
        description="Simple spider",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            spider.py -u http://192.168.122.131/mutillidae      # metasploitable
            spider.py -u https://example.com                    # outside lab
        """
        ),
    )
    parser.add_argument(
        "-u", "--url", default="http://192.168.122.131/mutillidae", help="target url"
    )
    values = parser.parse_args()
    return values


def extract_links_from(target_url):
    response = requests.get(target_url)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))


def crawl(target_url):
    href_links = extract_links_from(target_url)
    for link in href_links:
        # Convert relative links
        link = urlparse.urljoin(target_url, link)
        # Strip # markup
        link = link.split("#")[0]
        # Only local links and make unique
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


if __name__ == "__main__":

    options = get_args()
    target_links = []
    try:
        crawl(options.url)
    except KeyboardInterrupt:
        print("\n[+] Detected CTRL+C ... ")
        print("[+] Done")
