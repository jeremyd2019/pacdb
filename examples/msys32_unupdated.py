#!/usr/bin/env python

from glob import glob
from shutil import copy2

import pacdb

build32 = pacdb.Database.from_url('build32', 'https://github.com/jeremyd2019/msys2-build32/releases/download/repo')
msys32 = pacdb.msys_db_by_arch('i686')


for pkg in msys32:
    if pkg not in build32:
        filename = pkg.filename
        for fn in glob(f"msys/i686/{filename}*"):
            copy2(fn, "test")



