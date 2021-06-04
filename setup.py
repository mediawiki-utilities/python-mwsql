import os

from setuptools import setup, find_packages

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(base_dir, 'src')


# Fetch package metadata
about = {}
with open(os.path.join(SRC_DIR, "mwsql", "__about__.py")) as fh:
    exec(fh.read(), about)

with open(os.path.join(base_dir, "README.md")) as fh:
    long_description = fh.read()


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    keywords=['sql', 'dump', 'wikimedia', 'wikipedia'],
    long_description=long_description,
    long_description_content_type="text/x-md",
    license=about["__license__"],
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__email__"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Security :: Cryptography",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[]
)