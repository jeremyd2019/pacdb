#!/usr/bin/env python

import pacdb

REPO = "mingw64"
MINGW_PACKAGE_PREFIX = "mingw-w64-x86_64"
TOML = f"{MINGW_PACKAGE_PREFIX}-python-toml"
TOMLI = TOML + "i"

repo = pacdb.mingw_db_by_name(REPO)
for pkg in repo:
    deps = pkg.depends.keys() | pkg.makedepends.keys()
    if TOML in deps and TOMLI in deps:
        print(pkg.base)

