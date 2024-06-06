#!/usr/bin/env python

import os
import pacdb
from urllib.request import urlretrieve

clangarm64 = pacdb.mingw_db_by_name('clangarm64')

files = set()
for pkg in clangarm64:
    files.add(pkg.filename)
    url = "{}/{}".format(pkg.db.url, pkg.filename)
    filename = os.path.join("clangarm64", pkg.filename)
    try:
        s = os.stat(filename)
        if s.st_size == pkg.download_size:
            continue
    except FileNotFoundError:
        pass
    print(f"{url} -> {filename}")
    urlretrieve(url, filename)

toremove = [f for f in os.listdir("clangarm64") if f not in files]
#print(toremove)

for f in toremove:
    os.unlink(os.path.join("clangarm64", f))

