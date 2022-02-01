#!/usr/bin/env python3

import contextlib  # https://docs.python.org/3/library/contextlib.html
import os  # https://docs.python.org/3/library/os.html
import queue  # https://docs.python.org/3/library/queue.html
import requests  # https://docs.python-requests.org/en/master/
import sys  # https://docs.python.org/3/library/sys.html
import threading  # https://docs.python.org/3/library/threading.html
import time  # https://docs.python.org/3/library/time.html


FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET = "http://some/wordpress"
THREADS = 10

answers = queue.Queue()
web_paths = queue.Queue()


def gather_paths():
    for root, _, files in os.walk("."):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith("."):
                path = path[1:]
            print(path)
            web_paths.put(path)


@contextlib.contextmanager
def chdir(path):
    this_dir = os.getcwd()  # Original
    os.chdir(path)  # Set path
    try:
        yield
    finally:
        os.chdir(this_dir)  # Change path back to Original


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f"{TARGET}{path}"
        time.sleep(2)  # target may have throttling/lockout.
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write("+")
        else:
            sys.stdout.write("x")
        sys.stdout.flush()


def run():
    mythreads = list()
    for i in range(THREADS):
        print(f"[+] Spawning thread {i}")
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()

    for thread in mythreads:
        thread.join()


if __name__ == "__main__":
    with chdir("/home/<user>/Downloads/wordpress"):
        gather_paths()
    input("[+] Press return to continue.")

    run()
    with open("myanswers.txt", "w") as file:
        while not answers.empty():
            file.write(f"{answers.get()}\n")
    print("done")
