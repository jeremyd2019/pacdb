#!/usr/bin/env python

import re
import pacdb

pfxre = re.compile(r'^mingw-w64(?:-clang|-ucrt)?-(?:x86_64|i686|aarch64)-')

mingw64 = pacdb.mingw_db_by_name('mingw64')
ucrt64 = pacdb.mingw_db_by_name('ucrt64')


mingw64names = {pfxre.sub('mingw-w64-', pkg.name) for pkg in mingw64}

ucrt64names = {pfxre.sub('mingw-w64-', pkg.name) for pkg in ucrt64}

updates = mingw64names - ucrt64names


print(updates)

