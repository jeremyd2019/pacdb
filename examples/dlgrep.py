#!/usr/bin/env python

import os
import pacdb
import re

pkgconfre = re.compile(r'^[^/]+/(?:lib|share)/pkgconfig/.*\.pc$')
ldlre = re.compile(rb'\s-ldl\b')

for filename in os.listdir("clangarm64"):
    with pacdb.ExtTarFile.open(name=os.path.join("clangarm64", filename), mode="r:*") as tar:
        dlfcn = False
        builddate = None
        for info in tar:
            if info.name == ".BUILDINFO":
                infofile = tar.extractfile(info)
                with infofile:
                    buildinfo = infofile.read()
                    if b"installed = mingw-w64-clang-aarch64-dlfcn" in buildinfo and not filename.startswith("mingw-w64-clang-aarch64-ffmpeg") and b"installed = mingw-w64-clang-aarch64-mlt" not in buildinfo:
                        dlfcn = True
            elif info.name == ".PKGINFO" and dlfcn:
                infofile = tar.extractfile(info)
                with infofile:
                    for line in infofile.read().decode("utf-8").splitlines():
                        line = line.strip()
                        if not line.startswith("builddate = "):
                            continue
                        var, val = line.split(" = ", 1)
                        val = re.sub(r'\s+', ' ', val)
                        builddate = int(val)
                        print(builddate, "-", filename, ": dlfcn installed")

            elif pkgconfre.match(info.name):
                infofile = tar.extractfile(info)
                with infofile:
                    if ldlre.search(infofile.read()):
                        print(filename, ": -ldl in pkgconfig file")
