import os
from pathlib import Path, PosixPath
from urllib.error import HTTPError

import pytest

from mwsql.utils import _open_file, head, load

from .helpers import Capturing

CURRENT_DIR = Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"
FILEPATH_GZ = DATA_DIR / "testfile.sql.gz"
FILEPATH_UNZIPPED = DATA_DIR / "testfile.sql"


@pytest.mark.parametrize(
    "database,filename,date,extension,expected",
    [
        (
            "simplewiki",
            "change_tag_def",
            "latest",
            "sql",
            "simplewiki-latest-change_tag_def.sql.gz",
        ),
        (
            "simplewiki",
            "change_tag",
            "latest",
            "sql",
            "simplewiki-latest-change_tag.sql.gz",
        ),
        ("bewiki", "site_stats", "latest", "sql", "bewiki-latest-site_stats.sql.gz"),
        ("nlwiktionary", "sites", "latest", "sql", "nlwiktionary-latest-sites.sql.gz"),
    ],
)
def test_load(database, filename, date, extension, expected):
    f = load(database, filename, date, extension)
    assert f == PosixPath(expected)
    os.remove(f)


def test_load_HTTPError():
    with pytest.raises(HTTPError):
        load("simplewiki", "non-existing-filename", "latest")


def test__open_file_gz():
    with _open_file(FILEPATH_GZ) as infile:
        for line in infile:
            assert (
                line
                == "-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)\n"
            )
            break


def test__open_file_unzipped():
    with _open_file(FILEPATH_UNZIPPED) as infile:
        for line in infile:
            assert (
                line
                == "-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)\n"
            )
            break


expected_out = [
    "-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)",
    "--",
    "-- Host: 10.64.32.82    Database: simplewiki",
    "-- ------------------------------------------------------",
    "-- Server version\t10.4.19-MariaDB-log",
    "",
    "/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;",
    "/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;",
    "/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;",
    "/*!40101 SET NAMES utf8mb4 */;",
]


def test_head_gz():
    with Capturing() as output:
        head(FILEPATH_GZ, 10)
    assert output == expected_out


def test_head_unzipped():
    with Capturing() as output:
        head(FILEPATH_UNZIPPED, 10)
    assert output == expected_out
