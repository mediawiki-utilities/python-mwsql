import os
from pathlib import Path

import pytest

from mwsql.dump import Dump

# from .helpers import Capturing

CURRENT_DIR = Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"
FILEPATH_GZ = DATA_DIR / "testfile.sql.gz"
FILEPATH_UNZIPPED = DATA_DIR / "testfile.sql"


@pytest.fixture
def dump_gz():
    return Dump.from_file(FILEPATH_GZ)


@pytest.fixture
def dump_unzipped():
    return Dump.from_file(FILEPATH_UNZIPPED)


def test_from_file_gz(dump_gz):
    assert dump_gz.db == "simplewiki"
    assert dump_gz.name == "change_tag_def"
    assert dump_gz.col_names == ["ctd_id", "ctd_name", "ctd_user_defined", "ctd_count"]
    assert dump_gz.sql_dtypes == {
        "ctd_id": "int(10) unsigned NOT NULL AUTO_INCREMENT",
        "ctd_name": "varbinary(255) NOT NULL",
        "ctd_user_defined": "tinyint(1) NOT NULL",
        "ctd_count": "bigint(20) unsigned NOT NULL DEFAULT 0",
    }
    assert dump_gz.primary_key == ["ctd_id"]
    assert dump_gz.size == 2131
    assert dump_gz._dtypes is None
    assert dump_gz._source_file == FILEPATH_GZ
    assert dump_gz._encoding == "utf-8"


def test_from_file_unzipped(dump_unzipped):
    assert dump_unzipped.db == "simplewiki"
    assert dump_unzipped.name == "change_tag_def"
    assert dump_unzipped.col_names == [
        "ctd_id",
        "ctd_name",
        "ctd_user_defined",
        "ctd_count",
    ]
    assert dump_unzipped.sql_dtypes == {
        "ctd_id": "int(10) unsigned NOT NULL AUTO_INCREMENT",
        "ctd_name": "varbinary(255) NOT NULL",
        "ctd_user_defined": "tinyint(1) NOT NULL",
        "ctd_count": "bigint(20) unsigned NOT NULL DEFAULT 0",
    }
    assert dump_unzipped.primary_key == ["ctd_id"]
    assert dump_unzipped.size == 5082
    assert dump_unzipped._dtypes is None
    assert dump_unzipped._source_file == FILEPATH_UNZIPPED
    assert dump_unzipped._encoding == "utf-8"


def test_encoding(dump_gz):
    assert dump_gz.encoding == dump_gz._encoding == "utf-8"
    dump_gz.encoding = "latin-1"
    assert dump_gz.encoding == dump_gz._encoding == "latin-1"


def test_dtypes(dump_gz):
    assert dump_gz._dtypes is None
    assert (
        dump_gz.dtypes
        == dump_gz._dtypes
        == {"ctd_id": int, "ctd_name": str, "ctd_user_defined": int, "ctd_count": int}
    )


expected_out = [
    "['ctd_id', 'ctd_name', 'ctd_user_defined', 'ctd_count']",
    "['1', 'mw-replace', '0', '10200']",
    "['2', 'visualeditor', '0', '305860']",
    "['3', 'mw-undo', '0', '58220']",
    "['4', 'mw-rollback', '0', '70687']",
    "['5', 'mobile edit', '0', '230487']",
    "['6', 'mobile web edit', '0', '223010']",
    "['7', 'very short new article', '0', '28586']",
    "['8', 'visualeditor-wikitext', '0', '20113']",
    "['9', 'mw-new-redirect', '0', '29681']",
    "['10', 'visualeditor-switched', '0', '17717']",
]

expected_out_converted = [
    "['ctd_id', 'ctd_name', 'ctd_user_defined', 'ctd_count']",
    "[1, 'mw-replace', 0, 10200]",
    "[2, 'visualeditor', 0, 305860]",
    "[3, 'mw-undo', 0, 58220]",
    "[4, 'mw-rollback', 0, 70687]",
    "[5, 'mobile edit', 0, 230487]",
    "[6, 'mobile web edit', 0, 223010]",
    "[7, 'very short new article', 0, 28586]",
    "[8, 'visualeditor-wikitext', 0, 20113]",
    "[9, 'mw-new-redirect', 0, 29681]",
    "[10, 'visualeditor-switched', 0, 17717]",
]


def test_rows():
    pass


# @pytest.mark.parametrize(
#     "n_lines,convert,expected",
#     [
#         (5, False, expected_out[:5]),
#         (5, True, expected_out_converted[:5]),
#         (10, False, expected_out[:10]),
#         (10, True, expected_out_converted[:10]),
#     ],
# )
# def test_head(n_lines, convert, expected):
#     with Capturing() as output:
#         dump_gz.head(n_lines, convert)
#     assert output == expected


def test_head_no_exception(dump_gz, dump_unzipped):
    try:
        dump_gz.head(200)
        dump_unzipped.head(200)
    except StopIteration:
        pytest.fail("Unexpected StopIteration")


def test_to_csv(dump_gz):
    csv_filepath = CURRENT_DIR / "testfile.csv"
    # write CSV file
    dump_gz.to_csv(csv_filepath)
    with open(csv_filepath) as infile:
        content = infile.readlines()
    assert content[0] == "ctd_id,ctd_name,ctd_user_defined,ctd_count\n"
    assert content[1] == "1,mw-replace,0,10200\n"
    assert content[20] == "20,article with links to other-language wikis?,0,3556\n"
    assert content[50] == "83,repeated xwiki CoI abuse,0,48\n"
    assert content[-1] == "125,discussiontools-source-enhanced,0,341\n"
    os.remove(csv_filepath)
