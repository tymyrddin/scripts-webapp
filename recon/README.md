# Recon scripts

These recon scripts are made on and for Kali. The Kali Qemu VM runs a `zsh`, so the hashbang for these scripts is `#!/usr/bin/env bash`.

Editor used: [sublimetext](https://www.sublimetext.com/docs/linux_repositories.html).

## Usage recon.sh

    ./recon.sh -m [MODE] [domains]

* MODE can be `scan-only`, `dirsearch-only`, `crt-only`. Default is to run all three.
* Multiple domains possible (separate by space)

## Notes on dirsearch

Instead of using Kali's `dirsearch`, I cloned the latest `dirsearch.py` from GitHub in the same location as my script, 
making the path to the `dirsearch.py` script `dirsearch/dirsearch.py`, and in the `recon.sh` script setting a path 
variable. Easy changes.

    git clone https://github.com/maurosoria/dirsearch.git

And `dirsearch.py` comes with a dependency on `mysql-connector`, which is deprecated. Resolve with:

    pip install mysql-connector-python-rf

The `--simple-report` option is deprecated and replaced by the options `--format` and `-o`.
