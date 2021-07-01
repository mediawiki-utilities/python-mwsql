"""A set of utilities for processing MediaWiki SQL dump data"""

__version__ = "0.1.0.dev0"

import csv
import sys

from pathlib import Path
from typing import Any, Dict, List, Iterator, Optional, Union

from utils import open_file
from parser import has_sql_attribute, get_sql_attribute
from parser import map_dtypes, convert, parse

# Allow long field names
csv.field_size_limit(sys.maxsize)

# Custom types
TextFileGenerator = Iterator[str]
BinaryFileGenerator = Iterator[bytes]
FileGenerator = Union[TextFileGenerator, BinaryFileGenerator]
PathObject = Union[str, Path]


class Dump:
    """Class for parsing an SQL dump file and processing its contents"""

    def __init__(
        self,
        database: Optional[str],
        table_name: Optional[str],
        col_names: List[str],
        col_dtypes: Dict[str, str],
        primary_key: Optional[str],
        source_file: PathObject,
        encoding: str,
    ) -> None:

        self.db = database
        self.name = table_name
        self.col_names = col_names
        self.sql_dtypes = col_dtypes
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
        """Get the encoding used to read the dump file"""

        return self._encoding

    @encoding.setter
    def encoding(self, new_encoding: str) -> None:
        """Set the encoding used to read the dump file"""

        self._encoding = new_encoding

    @property
    def dtypes(self) -> Dict[str, type]:
        """Get a mapping between col_names and native Python dtypes"""

        if self._dtypes is None:
            self._dtypes = map_dtypes(self.sql_dtypes)
        return self._dtypes

    @classmethod
    def from_file(cls, file_path: PathObject, encoding: str = "utf-8"):
        """Initialize Dump object from dump file"""

        source_file = file_path
        database = None
        table_name = None
        primary_key = None
        col_names = []
        col_dtypes = {}

        if str(file_path).endswith(".gz"):
            infile = open_file(file_path, "rt", encoding=encoding)
        else:
            infile = open_file(file_path, "r", encoding=encoding)

        # Extract meta data from dump file
        for line in infile:
            if has_sql_attribute(line, "database"):
                database = get_sql_attribute(line, "database")

            elif has_sql_attribute(line, "create"):
                table_name = get_sql_attribute(line, "table_name")

            elif has_sql_attribute(line, "col_name"):
                col_name = get_sql_attribute(line, "col_name")
                dtype = get_sql_attribute(line, "dtype")
                col_names.append(col_name)
                col_dtypes[col_name] = dtype

            elif has_sql_attribute(line, "primary_key"):
                primary_key = get_sql_attribute(line, "primary_key")

            elif has_sql_attribute(line, "insert"):
                break

        return cls(
            database,
            table_name,
            col_names,  # type: ignore
            col_dtypes,  # type: ignore
            primary_key,
            source_file,
            encoding,
        )

    def rows(
        self, convert_dtypes: bool = False, strict: bool = False, **kwargs: Any
    ) -> Iterator[List[Any]]:
        """Create a generator object from the rows"""

        if str(self._source_file).endswith(".gz"):
            infile = open_file(self._source_file, "rt", encoding=self.encoding)
        else:
            infile = open_file(self._source_file, "r", encoding=self.encoding)

        if convert_dtypes:
            dtypes = list(self.dtypes.values())

        for line in infile:
            if has_sql_attribute(line, "insert"):
                rows = parse(line, **kwargs)
                for row in rows:
                    if convert_dtypes:
                        converted_row = convert(row, dtypes, strict=strict)
                        yield converted_row
                    else:
                        yield row

    def to_csv(self, file_path: PathObject, **kwargs: Any) -> None:
        """Write Dump object to CSV file"""

        with open(file_path, "w") as outfile:
            writer = csv.writer(outfile, **kwargs)
            writer.writerow(self.col_names)
            for row in self:
                writer.writerow(row)

    def head(self, n_lines: int = 10) -> None:
        """Display first n rows"""

        rows = self.rows()
        print(self.col_names)

        for _ in range(n_lines):
            try:
                print(next(rows))
            except StopIteration:
                return
        return
