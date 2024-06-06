#!/usr/bin/env python

import pacdb


clang64 = pacdb.mingw_db_by_name('clang64')

seen = set()
for pkg in clang64:
    if 'mingw-w64-clang-x86_64-gcc' in pkg.depends:
        if pkg.base not in seen:
            seen.add(pkg.base)
            print(pkg.base)

print("%d package bases\n" % len(seen))


import json
from urllib.request import urlopen

with urlopen("https://github.com/msys2/MINGW-packages/releases/download/srcinfo-cache/srcinfo.json") as fp:
    srcinfos = json.load(fp)

count = 0
for pkg in srcinfos.values():
    if 'clang64' in pkg['srcinfo']:
        srcinfo = pkg['srcinfo']['clang64']
        for line in srcinfo.split("\n"):
            line = line.lstrip()
            if not line:
                continue

            (name, value) = line.split(" = ", 1)
            if name in ('depends', 'makedepends') and value == 'mingw-w64-clang-x86_64-gcc':
                print(pkg['path'])
                count += 1

print("%d PKGBUILDs" % count)
