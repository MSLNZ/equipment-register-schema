"""Build the documentation to the docs/build directory.

Accepts the name of the release as a command-line argument.
If not specified, the name "develop" is used.

Build to the docs/build/develop directory
$ python build_docs.py

Build to the docs/build/v0.1.0 directory
$ python build_docs.py v0.1.0
"""

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "lxml",
# ]
# ///
import os
import re
import shutil
import sys
import zlib
from pathlib import Path
from subprocess import run

from lxml import __version__, etree

tag = "develop" if len(sys.argv) == 1 else sys.argv[1]

os.chdir("docs")

# write to stderr instead of stdout because stderr is where the
# Java log messages are written to
print(f"lxml version {__version__}", file=sys.stderr)

# Check that java is available
try:
    run(["java", "-version"])
except FileNotFoundError:
    sys.exit("You need java installed and available on PATH")

# Build SVG file
run(
    [
        "java",
        "-jar",
        "bin/xsdvi.jar",
        "../equipment-register.xsd",
        "-useStyle",
        "css/diagram.css",
    ],
)

# Copy styles and images to the new build directory
shutil.rmtree(f"build/{tag}", ignore_errors=True)
shutil.copytree("images", f"build/{tag}/images")
shutil.copytree("css", f"build/{tag}/css")
Path("equipment-register.svg").replace(f"build/{tag}/diagram.svg")

# Build HTML file
xsd = etree.parse("../equipment-register.xsd")
xsl = etree.parse("xs3p-msl.xsl")
transform = etree.XSLT(xsl)
result = transform(xsd)
result.write_output(f"build/{tag}/index.html")

# Update versions.json (only when running on GitHub Actions)
if os.getenv("GITHUB_ACTIONS") == "true":
    import json
    from urllib.request import urlopen, HTTPError

    owner, repo = os.environ["GITHUB_REPOSITORY"].split("/")
    version_file = "build/versions.json"
    versions: list[str] = []
    try:
        with urlopen(f"https://{owner}.github.io/{repo}/versions.json") as url:
            versions = json.load(url)
    except HTTPError:
        pass
    finally:
        if tag not in versions:
            versions.insert(1, tag)
            with open(version_file, "w") as fp:
                json.dump(versions, fp, indent=4)
            print(f"Inserted {tag!r} into {version_file}")

# Creates the objects.inv file (for inter-sphinx mapping)
inventory = []
with open(f"build/{tag}/index.html", encoding="utf-8") as f:
    hrefs = sorted(
        set(
            item["href"] for item in re.finditer(r'href="#(?P<href>[^"]+)"', f.read())
            if "_" in item["href"] and not item["href"].endswith("-collapse")
        )
    )

    for href in hrefs:
        role, name = href.split("_")
        inventory.append(f"{href} xsd:{role} 1 #{href} {name}".encode())

with open(f"build/{tag}/objects.inv", "wb") as f:
    f.write(b"# Sphinx inventory version 2\n")
    f.write(b"# Project: MSL-Equipment-Register-Schema\n")
    f.write(f"# Version: {xsd.getroot().attrib['version']}\n".encode())
    f.write(b"# The remainder of this file is compressed using zlib.\n")
    f.write(zlib.compress(b"\n".join(inventory) + b"\n", 9))

print(f"Saved to docs/build/{tag}")
