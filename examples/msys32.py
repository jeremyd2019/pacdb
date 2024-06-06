#!/usr/bin/env python

import pacdb

build32 = pacdb.Database.from_url('build32', 'https://github.com/jeremyd2019/msys2-build32/releases/download/repo')
msys64 = pacdb.msys_db_by_arch('x86_64')
msys32 = pacdb.msys_db_by_arch('i686')


combined32 = {pkg.name: pkg for pkg in msys32}
combined32.update({pkg.name: pkg for pkg in build32})

pkgs64 = {str(pkg): pkg for pkg in msys64}
pkgs32 = {str(pkg): pkg for pkg in combined32.values()}

updates = pkgs64.keys() - pkgs32.keys()

def base(pkg):
    return pkg.base or pkg.name

print(" ".join(sorted({base(pkgs64[fullname]) for fullname in updates})))


