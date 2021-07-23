"""
A set of utilities for processing MediaWiki SQL dump data.
"""

import csv
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Type, TypeVar, Union

from .parser import (
    _convert,
    _get_sql_attribute,
    _has_sql_attribute,
    _map_dtypes,
    _parse,
)
from .utils import _open_file

# Allow long field names
csv.field_size_limit(sys.maxsize)

# Custom types
PathObject = Union[str, Path]
T = TypeVar("T", bound="Dump")


class Dump:
    """
    Class for parsing an SQL dump file and processing its contents.
    """

    def __init__(
        self,
        database: Optional[str],
        table_name: Optional[str],
        col_names: List[str],
        col_sql_dtypes: Dict[str, str],
        primary_key: Optional[str],
        source_file: PathObject,
        encoding: str,
    ) -> None:
        """
        Dump class constructor.

        :param database: The wiki database, e.g. 'enwiki' or 'dewikibooks'
        :type database: Optional[str]
        :param table_name: The SQL table name
        :type table_name: Optional[str]
        :param col_names: The SQL table column (field) names
        :type col_names: List[str]
        :param col_sql_dtypes: A mapping from the column names in a SQL table
            to their respective SQL data types.
            Example: {"ct_id": int(10) unsigned NOT NULL AUTO_INCREMENT}
        :type col_sql_dtypes: Dict[str, str]
        :param primary_key: The primary key of the SQL table
            Can be unique or composite.
        :type primary_key: Optional[str]
        :param source_file: The path to the SQL dump file
        :type source_file: PathObject
        :param encoding: Text encoding
        :type encoding: str
        """

        self.db = database
        self.name = table_name
        self.col_names = col_names
        self.sql_dtypes = col_sql_dtypes
        self.primary_key = primary_key
        self.size = Path(source_file).stat().st_size
        self._dtypes: Optional[Dict[str, type]] = None
        self._source_file = source_file
        self._encoding = encoding

    def __str__(self) -> str:
        return f"Dump(database={self.db}, name={self.name}, size={self.size})"

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self) -> Iterator[List[Any]]:
        return self.rows()

    @property
    def encoding(self) -> str:
        """
        The encoding used to read the dump file.

        :getter: Returns the current encoding
        :setter: Sets the encoding to a new value
        :return: Text encoding
        :rtype: str
        """

        return self._encoding

    @encoding.setter
    def encoding(self, new_encoding: str) -> None:

        self._encoding = new_encoding

    @property
    def dtypes(self) -> Dict[str, type]:
        """
        Mapping between col_names and native Python dtypes.

        :return: A mapping from the column names in a SQL table
            to their respective Python data types. Example: {"ct_id": int}
        :rtype: Dict[str, type]
        """

        if self._dtypes is None:
            self._dtypes = _map_dtypes(self.sql_dtypes)
        return self._dtypes

    @classmethod
    def from_file(cls: Type[T], file_path: PathObject, encoding: str = "utf-8") -> T:
        """
        Initialize Dump object from dump file.

        :param cls: A Dump class instance
        :type cls: Dump
        :param file_path: Path to source SQL dum file. Can be a .gz or an
            uncompressed file
        :type file_path: PathObject
        :param encoding: Text encoding, defaults to "utf-8" If you get
            an encoding error when processing the file, try setting this
            parameter to 'Latin-1'
        :type encoding: str, optional
        :return: A Dump class instance
        :rtype: Dump
        """

        source_file = file_path
        database = None
        table_name = None
        primary_key = None
        col_names = []
        col_sql_dtypes = {}

        # Extract meta data from dump file
        with _open_file(file_path, encoding=encoding) as infile:
            for line in infile:
                if _has_sql_attribute(line, "database"):
                    database = _get_sql_attribute(line, "database")

                elif _has_sql_attribute(line, "create"):
                    table_name = _get_sql_attribute(line, "table_name")

                elif _has_sql_attribute(line, "col_name"):
                    col_name = _get_sql_attribute(line, "col_name")
                    dtype = _get_sql_attribute(line, "dtype")
                    col_names.append(col_name)
                    col_sql_dtypes[col_name] = dtype

                elif _has_sql_attribute(line, "primary_key"):
                    primary_key = _get_sql_attribute(line, "primary_key")

                elif _has_sql_attribute(line, "insert"):
                    break

            return cls(
                database,
                table_name,
                col_names,  # type: ignore
                col_sql_dtypes,  # type: ignore
                primary_key,
                source_file,
                encoding,
            )

    def rows(
        self,
        convert_dtypes: bool = False,
        strict_conversion: bool = False,
        **fmtparams: Any,
    ) -> Iterator[List[Any]]:
        """
        Create a generator object from the rows.

        :param convert_dtypes: When set to True, numerical types are
            converted from str to int or float. Defaults to False.
        :type convert_dtypes: bool, optional
        :param strict_conversion: When True, raise exception Error on
            bad input when converting from SQL dtypes to Python dtypes.
            Defaults to False.
        :type strict_conversion: bool, optional
        :param fmtparams: Any kwargs you want to pass to the csv.reader()
            function that does the actual parsing.
        :yield: A generator used to iterate over the rows in the SQL table
        :rtype: Iterator[List[Any]]
        """

        if convert_dtypes:
            dtypes = list(self.dtypes.values())

        with _open_file(self._source_file, encoding=self.encoding) as infile:
            for line in infile:
                if _has_sql_attribute(line, "insert"):
                    rows = _parse(line, **fmtparams)
                    for row in rows:
                        if convert_dtypes:
                            converted_row = _convert(
                                row, dtypes, strict=strict_conversion
                            )
                            yield converted_row
                        else:
                            yield row

    def to_csv(self, file_path: PathObject, **fmtparams: Any) -> None:
        """
        Write Dump object to CSV file.

        :param file_path: The file to write to. Will be created if it
            doesn't already exist. Will be overwritten if it does exist.
        :type file_path: PathObject
        """

        with open(file_path, "w") as outfile:
            writer = csv.writer(outfile, **fmtparams)
            writer.writerow(self.col_names)
            for row in self:
                writer.writerow(row)

    def head(self, n_lines: int = 10, convert_dtypes: bool = False) -> None:
        """
        Display first n rows.

        :param n_lines: Number of rows to display, defaults to 10
        :type n_lines: int, optional
        :param convert_dtypes: Optionally, shows numerical types as int
            or float instead of all str. Defaults to False.
        :type convert_dtypes: bool, optional
        """

        rows = self.rows(convert_dtypes=convert_dtypes)
        print(self.col_names)

        for _ in range(n_lines):
            try:
                print(next(rows))
            except StopIteration:
                return
        return
