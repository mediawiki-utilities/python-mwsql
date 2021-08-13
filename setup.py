# type: ignore
from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent.resolve()
SRC_DIR = BASE_DIR / "src"

# Get package metadata
about = {}
with open(SRC_DIR / "mwsql" / "about.py") as fh:
    exec(fh.read(), about)

# Get long description from README
long_description = (BASE_DIR / "README.rst").read_text(encoding="utf-8")


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    keywords=["sql", "dump", "wikimedia", "wikipedia"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license=about["__license__"],
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__email__"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["wget >= 3.2"],
    include_package_data=True,
    zip_safe=False,
)
