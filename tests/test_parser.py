import pytest

from mwsql.parser import (
    _convert,
    _get_sql_attribute,
    _has_sql_attribute,
    _map_dtypes,
    _parse,
    _split_tuples,
)

metadata = {
    0: "-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)",
    1: "--",
    2: "-- Host: 10.64.32.82    Database: simplewiki",
    3: "-- ------------------------------------------------------",
    4: "-- Server version\t10.4.19-MariaDB-log",
    5: "",
    6: "/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;",
    7: "/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;",
    8: "/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;",
    9: "/*!40101 SET NAMES utf8mb4 */;",
    10: "/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;",
    11: "/*!40103 SET TIME_ZONE='+00:00' */;",
    12: "/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;",
    13: "/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;",
    14: "/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;",
    15: "/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;",
    16: "",
    17: "--",
    18: "-- Table structure for table `change_tag_def`",
    19: "--",
    20: "",
    21: "DROP TABLE IF EXISTS `change_tag_def`;",
    22: "/*!40101 SET @saved_cs_client     = @@character_set_client */;",
    23: "/*!40101 SET character_set_client = utf8 */;",
    24: "CREATE TABLE `change_tag_def` (",
    25: "`ctd_id` int(10) unsigned NOT NULL AUTO_INCREMENT,",
    26: "`ctd_name` varbinary(255) NOT NULL,",
    27: "`ctd_user_defined` tinyint(1) NOT NULL,",
    28: "`ctd_count` bigint(20) unsigned NOT NULL DEFAULT 0,",
    29: "PRIMARY KEY (`ctd_id`),",
    30: "UNIQUE KEY `ctd_name` (`ctd_name`),",
    31: "KEY `ctd_count` (`ctd_count`),",
    32: "KEY `ctd_user_defined` (`ctd_user_defined`)",
    33: ") ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=binary;",
    34: "/*!40101 SET character_set_client = @saved_cs_client */;",
    35: "",
    36: "--",
    37: "-- Dumping data for table `change_tag_def`",
    38: "--",
    39: "",
    40: "/*!40000 ALTER TABLE `change_tag_def` DISABLE KEYS */;",
    41: "INSERT INTO `change_tag_def` VALUES (1,'mw-replace',0,10200),(2,'visualeditor',0,305860)",
}


@pytest.mark.parametrize(
    "line,attr,expected",
    [
        (metadata[0], "database", False),
        (metadata[2], "database", True),
        (metadata[18], "create", False),
        (metadata[24], "create", True),
        (metadata[23], "col_name", False),
        (metadata[26], "col_name", True),
        (metadata[30], "primary_key", False),
        (metadata[29], "primary_key", True),
        (metadata[37], "insert", False),
        (metadata[41], "insert", True),
    ],
)
def test__has_sql_attribute(line, attr, expected):
    assert _has_sql_attribute(line, attr) == expected


@pytest.mark.parametrize(
    "line,attr,expected",
    [
        (metadata[2], "database", "simplewiki"),
        (metadata[24], "table_name", "change_tag_def"),
        (metadata[26], "col_name", "ctd_name"),
        (metadata[27], "dtype", "tinyint(1) NOT NULL"),
        (metadata[29], "primary_key", ["ctd_id"]),
    ],
)
def test__get_sql_attribute(line, attr, expected):
    assert _get_sql_attribute(line, attr) == expected


sql_dtypes = {
    "ctd_id": "int(10) unsigned NOT NULL AUTO_INCREMENT",
    "ctd_name": "varbinary(255) NOT NULL",
    "ctd_user_defined": "tinyint(1) NOT NULL",
    "ctd_count": "bigint(20) unsigned NOT NULL DEFAULT 0",
    "page_namespace": "int(11) NOT NULL DEFAULT 0",
    "page_title": "varbinary(255) NOT NULL DEFAULT ''",
    "page_restrictions": "tinyblob DEFAULT NULL",
    "page_is_redirect": "tinyint(1) unsigned NOT NULL DEFAULT 0",
    "page_is_new": "tinyint(1) unsigned NOT NULL DEFAULT 0",
    "page_random": "double unsigned NOT NULL DEFAULT 0",
    "page_touched": "varbinary(14) NOT NULL",
    "page_links_updated": "varbinary(14) DEFAULT NULL",
    "page_latest": "int(8) unsigned NOT NULL DEFAULT 0",
    "page_len": "int(8) unsigned NOT NULL DEFAULT 0",
    "page_content_model": "varbinary(32) DEFAULT NULL",
    "page_lang": "varbinary(35) DEFAULT NULL",
}

dtypes = {
    "ctd_id": int,
    "ctd_name": str,
    "ctd_user_defined": int,
    "ctd_count": int,
    "page_namespace": int,
    "page_title": str,
    "page_restrictions": str,
    "page_is_redirect": int,
    "page_is_new": int,
    "page_random": float,
    "page_touched": str,
    "page_links_updated": str,
    "page_latest": int,
    "page_len": int,
    "page_content_model": str,
    "page_lang": str,
}


def test__map_dtypes():
    assert _map_dtypes(sql_dtypes) == dtypes


convert_testdata = [
    [
        "8",
        "4",
        "Project_scope",
        "0",
        "0.575193598203",
        "20210624025721",
        "24941",
        "wikitext",
        "",
    ],  # Should pass without raising errors or warnings in both strict and non-strict mode
    [
        "bad value",
        "4",
        "Project_scope",
        "0",
        "0.575193598203",
        "20210624025721",
        "24941",
        "wikitext",
        "",
    ],  # First field is of the wrong type, should raise ValueError in strict mode and raise a warning in non-strict mode
    [
        "8",
        "4",
        "Project_scope",
        "0.575193598203",
        "20210624025721",
        "24941",
        "wikitext",
        "",
    ],  # One field is missing, should raise ValueError in strict mode
]
expected_output = [
    [8, 4, "Project_scope", 0, 0.575193598203, "20210624025721", 24941, "wikitext", ""],
    [
        "bad value",
        4,
        "Project_scope",
        0,
        0.575193598203,
        "20210624025721",
        24941,
        "wikitext",
        "",
    ],
    [
        "8",
        "4",
        "Project_scope",
        "0.575193598203",
        "20210624025721",
        "24941",
        "wikitext",
        "",
    ],
]

conv_dtypes = [int, int, str, int, float, str, int, str, str]


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (convert_testdata[0], expected_output[0]),
        (convert_testdata[2], expected_output[2]),
    ],
)
def test__convert_non_strict(input_data, expected):
    assert _convert(input_data, conv_dtypes, strict=False) == expected


def test__convert_raise_value_error_wrong_dtype():
    with pytest.raises(ValueError):
        _convert(convert_testdata[1], conv_dtypes, strict=True)


def test__convert_raise_warning_wrong_dtype():
    with pytest.warns(UserWarning):
        _convert(convert_testdata[1], conv_dtypes, strict=False)


def test__convert_raise_value_error_wrong_length():
    with pytest.raises(ValueError):
        _convert(convert_testdata[2], conv_dtypes, strict=True)


tuples_testdata = [
    "INSERT INTO `page` VALUES (10,0,'AccessibleComputing','',1,0,0.33167112649574004,'20210607122734','20210606191631',1002250816,111,'wikitext',NULL),(12,0,'Anarchism','',0,0,0.786172332974311,'20210701093040','20210701093138',1030472204,96584,'wikitext',NULL)",
    "INSERT INTO `page` VALUES (289,0,'ActresseS','',1,0,0.8987093492399061,'20210607122734','20210606191634',907518426,109,'wikitext',NULL),(290,0,'A','',0,0,0.854180265082214,'20210629155037','20210629155404',1031061699,28174,'wikitext',NULL),(291,0,'AnarchoCapitalism','',1,0,0.574773308424999,'20210621014117','20210606191634',783865104,86,'wikitext',NULL);",
]

expected_split = [
    [
        "10,0,'AccessibleComputing','',1,0,0.33167112649574004,'20210607122734','20210606191631',1002250816,111,'wikitext',",
        "12,0,'Anarchism','',0,0,0.786172332974311,'20210701093040','20210701093138',1030472204,96584,'wikitext',",
    ],
    [
        "289,0,'ActresseS','',1,0,0.8987093492399061,'20210607122734','20210606191634',907518426,109,'wikitext',",
        "290,0,'A','',0,0,0.854180265082214,'20210629155037','20210629155404',1031061699,28174,'wikitext',",
        "291,0,'AnarchoCapitalism','',1,0,0.574773308424999,'20210621014117','20210606191634',783865104,86,'wikitext',",
    ],
]

expected_parse = [
    [
        "10",
        "0",
        "AccessibleComputing",
        "",
        "1",
        "0",
        "0.33167112649574004",
        "20210607122734",
        "20210606191631",
        "1002250816",
        "111",
        "wikitext",
        "",
    ],
    [
        "289",
        "0",
        "ActresseS",
        "",
        "1",
        "0",
        "0.8987093492399061",
        "20210607122734",
        "20210606191634",
        "907518426",
        "109",
        "wikitext",
        "",
    ],
]


@pytest.mark.parametrize(
    "tuples_testdata,expected_split",
    [
        (tuples_testdata[0], expected_split[0]),
        (tuples_testdata[1], expected_split[1]),
    ],
)
def test__split_tuples(tuples_testdata, expected_split):
    assert _split_tuples(tuples_testdata) == expected_split


@pytest.mark.parametrize(
    "tuples_testdata,expected_parse",
    [
        (tuples_testdata[0], expected_parse[0]),
        (tuples_testdata[1], expected_parse[1]),
    ],
)
def test__parse(tuples_testdata, expected_parse):
    assert next(_parse(tuples_testdata)) == expected_parse
