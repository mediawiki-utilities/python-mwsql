"""
Utility functions used to download, open and display
the contents of Wikimedia SQL dump files.
"""

import gzip
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, TextIO, Union
from urllib.error import HTTPError

import wget  # type: ignore

# Custom type
PathObject = Union[str, Path]


@contextmanager
def _open_file(
    file_path: PathObject, encoding: Optional[str] = None
) -> Iterator[TextIO]:
    """
    Custom context manager for opening both .gz and uncompressed files.

    :param file_path: The path to the file
    :type file_path: PathObject
    :param encoding: Text encoding, defaults to None
    :type encoding: Optional[str], optional
    :yield: A file handle
    :rtype: Iterator[TextIO]
    """

    if str(file_path).endswith(".gz"):
        infile = gzip.open(file_path, mode="rt", encoding=encoding)
    else:
        infile = open(file_path, mode="r", encoding=encoding)
    try:
        yield infile
    finally:
        infile.close()


def head(file_path: PathObject, n_lines: int = 10, encoding: str = "utf-8") -> None:
    """
    Display first n lines of a file. Works with both
    .gz and uncompressed files. Defaults to 10 lines.

    :param file_path: The path to the file
    :type file_path: PathObject
    :param n_lines: Lines to display, defaults to 10
    :type n_lines: int, optional
    :param encoding: Text encoding, defaults to "utf-8"
    :type encoding: str, optional
    """

    with _open_file(file_path, encoding=encoding) as infile:
        for line in infile:
            if n_lines == 0:
                break
            try:
                print(line.strip())
                n_lines -= 1
            except StopIteration:
                return
    return


def _progress_bar(
    current: Union[int, float], total: Union[int, float], width: int = 60
) -> None:
    """
    Custom progress bar for wget downloads.

    :param current: bytes downloaded so far
    :type current: Union[int, float]
    :param total: Total size of download in bytes or megabytes
    :type total: Union[int, float]
    :param width: Progress bar width in chars, defaults to 60
    :type width: int, optional
    """

    unit = "bytes"

    # Show file size in MB for large files
    if total >= 100000:
        MB = 1024 * 1024
        current = current / MB
        total = total / MB
        unit = "MB"

    progress = current / total
    progress_message = f"Progress: \
    {progress:.0%} [{current:.1f} / {total:.1f}] {unit}"
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def load(
    database: str, filename: str, date: str = "latest", extension: str = "sql"
) -> Optional[PathObject]:
    """
    Load a dump file from a Wikimedia public directory if the
    user is in a supported environment (PAWS, Toolforge...). Otherwise, download dump file from the web and save in the current working directory. In both cases,the function returns a path-like object which can be used to access the file. Does not check if the file already exists on the path.

    :param database: The database backup dump to download a file from,
        e.g. 'enwiki' (English Wikipedia). See a list of available
        databases here: https://dumps.wikimedia.org/backup-index-bydb.html
    :type database: str
    :param filename: The name of the file to download, e.g. 'page' loads the
        file {database}-{date}-page.sql.gz
    :type filename: str
    :param date: Date the dump was generated, defaults to "latest". If "latest"
        is not used, the date format should be "YYYYMMDD"
    :type date: str, optional
    :param extension: The file extension. Defaults to 'sql'
    :type extension: str
    :return: Path to dump file
    :rtype: Optional[PathObject]
    """

    paws_root_dir = Path("/public/dumps/public/")
    dumps_url = "https://dumps.wikimedia.org/"
    subdir = Path(database, date)
    extended_filename = f"{database}-{date}-{filename}.{extension}.gz"
    file_path = Path(extended_filename)

    if paws_root_dir.exists():
        dump_file = Path(paws_root_dir, subdir, file_path)

    else:
        url = f"{dumps_url}{str(subdir)}/{str(file_path)}"
        try:
            print(f"Downloading {url}")
            dump_file = wget.download(url, bar=_progress_bar)
        except HTTPError as e:
            print(f"HTTPError: {e}")
            raise

    return Path(dump_file)
