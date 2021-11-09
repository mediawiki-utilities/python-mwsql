"""
Utility functions used to download, open and display
the contents of Wikimedia SQL dump files.
"""

import gzip
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, TextIO, Union

import requests  # type: ignore
from tqdm import tqdm  # type: ignore

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


def download_file(url: str, file_name: str) -> Optional[Path]:
    """
    Download a file from a URL and show a progress indicator. Return the path to the downloaded file.
    :param url: URL to download from
    :param file_name: name of the file to download
    :return: path to the downloaded file
    """

    session = requests.Session()
    response = session.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    block_size = 4096
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)

    with open(file_name, "wb") as outfile:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            outfile.write(data)
    progress_bar.close()

    if total_size != 0 and progress_bar.n != total_size:
        raise RuntimeError(
            f"Downloaded {progress_bar.n} bytes, expected {total_size} bytes"
        )

    return Path(file_name)


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
        return Path(paws_root_dir, subdir, file_path)

    else:
        url = f"{dumps_url}{str(subdir)}/{str(extended_filename)}"
        return download_file(url, extended_filename)
