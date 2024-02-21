import os
import re
import argparse
import sys
from subprocess import PIPE, run
from distutils.version import StrictVersion
import shutil

version_regex = re.compile(r"(?<=version=\")([\d\.]+)(?=\")")

python_exe = sys.executable

parser = argparse.ArgumentParser()
parser.add_argument("--test", "-t", action="store_true")
parser.add_argument("--debug", "-d", action="store_true")
parser.add_argument("--version", "-v", action="store")
args = parser.parse_args()

if args.test:
    repository_url = "https://test.pypi.org/legacy/"
else:
    repository_url = "https://upload.pypi.org/legacy/"

if args.debug:
    out = None
else:
    out = PIPE

with open("setup.py", "r+") as f:
    setup_py = f.read()
    matches = version_regex.search(setup_py)
    version = StrictVersion(matches.group(1))
    version = StrictVersion(f"{version.version[0]}.{version.version[1]}.{version.version[2]+1}")
    if args.version:
        version = StrictVersion(args.version)
    version = str(version)
    if len(version.split(".")) < 3:
        version += ".0"
    setup_py = version_regex.sub(version, setup_py)
    f.seek(0)
    f.write(setup_py)
    f.truncate()
if os.path.exists("dist"):
    shutil.rmtree("dist")

result = run(
    f"{python_exe} setup.py sdist bdist_wheel",
    stdout=out,
    universal_newlines=True,
    shell=True,
)
if result.returncode != 0:
    raise Exception("Could not execute build")


result = run(
    f"{python_exe} -m twine upload --repository-url {repository_url} dist/*",
    universal_newlines=True,
    shell=True,
)
if result.returncode != 0:
    raise Exception("Could not upload build")