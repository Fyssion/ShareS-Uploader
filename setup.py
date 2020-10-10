import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = ""
with open("shares_uploader/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("version is not set")

if version.endswith(("a", "b", "rc")):
    # append version identifier based on commit count
    try:
        import subprocess

        p = subprocess.Popen(
            ["git", "rev-list", "--count", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += out.decode("utf-8").strip()
        p = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except Exception:
        pass


setuptools.setup(
    name="shares-uploader",
    version=version,
    author="Fyssion",
    author_email="fyssioncodes@gmail.com",
    description="GUI and CLI that allows me to upload to my image server from ubuntu ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fyssion/shares-uploader",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
