#!/usr/bin/env python

import argparse
import os
import pacdb
import sys
# TODO: urlretrieve seems quite slow... possibly because urllib doesn't do
# persistent http connections.  investigate other libraries (requests?)
from urllib.request import urlretrieve
from urllib.error import HTTPError

parser = argparse.ArgumentParser(description='Mirror packages from a pacman sync db')
parser.add_argument('-e', '--repo', required=True, help='pacman repo name to mirror')
parser.add_argument('-v', '--verbose', action='count', help='output additional information')
parser.add_argument('url', help='source url')
parser.add_argument('dir', help='destination dir')

options = parser.parse_args()

db = pacdb.Database.from_url(options.repo, options.url)


def fetch_file(url, filename, expected_size=None):
    fetch = True
    try:
        s = os.stat(filename)
        if expected_size is None or s.st_size == expected_size:
            fetch = False
    except FileNotFoundError:
        pass
    if fetch:
        if options.verbose:
            print(f"{url} -> {filename}", file=sys.stderr)
        urlretrieve(url, filename)

files = set()
# unfortunately, I don't think there's any way to know the .tar.X extension,
# so just get the straight .db and .files without the extra extensions
for t in (".db", ".files"):
    files.add(options.repo + t)
    url = "{}/{}".format(db.url, options.repo + t)
    filename = os.path.join(options.dir, options.repo + t)
    fetch_file(url, filename, -1)
    try:
        url+=".sig"
        filename+=".sig"
        fetch_file(url, filename, -1)
        files.add(options.repo + t + ".sig")
    except HTTPError as e:
        if options.verbose:
            print(f"Warning: error retrieving {url}: {e}", file=sys.stderr)

for pkg in db:
    files.add(pkg.filename)
    url = "{}/{}".format(pkg.db.url, pkg.filename)
    filename = os.path.join(options.dir, pkg.filename)
    fetch_file(url, filename, pkg.download_size)
    try:
        url+=".sig"
        filename+=".sig"
        fetch_file(url, filename)
        files.add(pkg.filename + ".sig")
    except HTTPError as e:
        if options.verbose:
            print(f"Warning: error retrieving {url}: {e}", file=sys.stderr)

toremove = [f for f in os.listdir(options.dir) if f not in files]
if options.verbose and toremove:
    print("Removing:", "\n\t".join(toremove), sep="\n\t", file=sys.stderr)

for f in toremove:
    os.unlink(os.path.join(options.dir, f))

