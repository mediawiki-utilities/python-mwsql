"""Utility functions used to download, open and display
 the contents of SQL dump files. Works with both .gz and
 uncompressed files.
"""

import gzip
import sys
import wget  # type: ignore

from pathlib import Path
from typing import Iterator, Optional, Union
from urllib.error import HTTPError

# Custom types
# TextFileGenerator = Iterator[str]
# BinaryFileGenerator = Iterator[bytes]
# FileGenerator = Union[TextFileGenerator, BinaryFileGenerator]
PathObject = Union[str, Path]


# TODO: eventually will want to update the function calls to match rest of library -- e.g., file_path: string, mode: string, etc.
# Done!
def open_file(
    file_path: PathObject, mode: str, encoding: Optional[str] = None
) -> Iterator[str]:
    """Open file and return a file handle. Works with both
    .gz and uncompressed files.
    """

    # if "b" in mode and encoding is not None:
    #     raise ValueError("Argument 'encoding' not supported in binary mode")

    if str(file_path).endswith(".gz"):
        with gzip.open(file_path, mode, encoding=encoding) as file_handle:
            yield from file_handle
    else:
        with open(file_path, mode, encoding=encoding) as file_handle:
            yield from file_handle


def head(
    file_path: PathObject, n_lines: int = 10, encoding: str = "utf-8"
) -> None:
    """Display first n lines of a file. Works with both
    .gz and uncompressed files. Defaults to 10 lines.
    """

    if str(file_path).endswith(".gz"):
        infile = open_file(file_path, "rt", encoding=encoding)
    else:
        infile = open_file(file_path, "r", encoding=encoding)

    for line in infile:
        if n_lines == 0:
            break
        try:
            print(line.strip())
            n_lines -= 1
        except StopIteration:
            return
    return


# Minor but I would just get rid of the width parameter if you aren't going to use it
# I tried but wget wouldn't work without it. Haven't actually looked into it,
# but what I *think* happens is that while the progress_bar func itself doesn't use the width param, it gets passed as a kwarg to wget where it's necessary.
def progress_bar(
    current: Union[int, float], total: Union[int, float], width: int = 60
) -> None:
    """Custom progress bar for wget downloads"""

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


def load(database: str, filename: str) -> Optional[PathObject]:
    """Load dump file from public dir if in PAWS, else download
    from the web. Returns a file object.
    """

    # style: generally I only use ALL_CAPS variables when it's global so I would just change these to normal_var_names
    # Oh, cool! I though all caps were for constants in general but TIL
    # they're specifically for module level constants
    paws_root_dir = Path("/public/dumps/public/")
    dumps_url = "https://dumps.wikimedia.org/"
    subdir = Path(database, "latest")
    extended_filename = f"{database}-latest-{filename}.sql.gz"
    file_path = Path(extended_filename)

    if paws_root_dir.exists():
        dump_file = Path(paws_root_dir, subdir, file_path)

    else:
        url = f"{dumps_url}{str(subdir)}/{str(file_path)}"
        try:
            print(f"Downloading {url}")
            dump_file = wget.download(url, bar=progress_bar)
        except HTTPError:
            print("File not found")
            return None

    return Path(dump_file)
