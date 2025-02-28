#!/usr/bin/python2.7

import os
import fileinput

# the version of the release
with open("version.txt") as f: version = f.read()

def getVersionTuple(v):
    return tuple(map(int, (v.split("."))))

version_major = str(getVersionTuple(version)[0])
version_minor = str(getVersionTuple(version)[1])
version_patch = str(getVersionTuple(version)[2])

# update version in the header file
print("updating the version in the header file")
doctest_contents = ""
for line in fileinput.input(["../doctest/parts/doctest_fwd.h"]):
    if line.startswith("#define DOCTEST_VERSION_MAJOR "):
        doctest_contents += f"#define DOCTEST_VERSION_MAJOR {version_major}" + "\n"
    elif line.startswith("#define DOCTEST_VERSION_MINOR "):
        doctest_contents += f"#define DOCTEST_VERSION_MINOR {version_minor}" + "\n"
    elif line.startswith("#define DOCTEST_VERSION_PATCH "):
        doctest_contents += f"#define DOCTEST_VERSION_PATCH {version_patch}" + "\n"
    else:
        doctest_contents += line

with open("../doctest/parts/doctest_fwd.h", "w") as readme:
    readme.write(doctest_contents)
# update meson file with version
print("updating the meson file")
meson_contents = "".join(
    f"project('doctest', ['cpp'], version: '{version}" + "')\n"
    if line.startswith("project('doctest'")
    else line
    for line in fileinput.input(["../meson.build"])
)
with open("../meson.build", "w") as meson:
    meson.write(meson_contents)
