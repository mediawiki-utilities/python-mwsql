# type: ignore
import os

from setuptools import find_packages, setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")


# Fetch package metadata
about = {}
with open(os.path.join(SRC_DIR, "mwsql", "about.py")) as fh:
    exec(fh.read(), about)

# Fetch long description from README
with open(os.path.join(BASE_DIR, "README.rst")) as fh:
    long_description = fh.read()


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
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["wget" >= 3.2],
    include_package_data=True,
    zip_safe=False,
)
