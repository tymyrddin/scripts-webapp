#!/usr/bin/env python3

import argparse  # https://docs.python.org/3/library/argparse.html
import requests  # https://docs.python-requests.org/en/master/
import textwrap  # https://docs.python.org/3/library/textwrap.html


def get_args():
    parser = argparse.ArgumentParser(
        description="Simple crawler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example: 
            crawler.py -u 192.168.122.131/mutillidae -t dirs    # metasploitable
            crawler.py -u google.com -t subdomains              # outside lab
        """
        ),
    )
    parser.add_argument("-u", "--url", default="192.168.122.131/mutillidae", help="target url")
    parser.add_argument("-t", "--type", default="dirs", help="crawl type: subdomains, dirs")
    values = parser.parse_args()
    return values


def request(target_url):
    try:
        return requests.get("http://" + target_url)
    except requests.exceptions.ConnectionError:
        pass


def discover_subdomains(target_url):
    print("[+] Crawling for subdomains")
    with open("subdomains-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + target_url
            response = request(test_url)
            if response:
                print("[+] Discovered subdomain: " + test_url)
        print("[+] Done")


def discover_hidden_dirs(target_url):
    print("[+] Crawling for hidden directories")
    with open("files-and-dirs-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url + "/" + word
            response = request(test_url)
            if response:
                print("[+] Discovered directory: " + test_url)
        print("[+] Done")


if __name__ == "__main__":

    options = get_args()
    try:
        if options.type == "dirs":
            discover_hidden_dirs(options.url)
        elif options.type == "subdomains":
            discover_subdomains(options.url)
    except KeyboardInterrupt:
        print("\n[+] Detected CTRL+C ... ")
        print("[+] Done")