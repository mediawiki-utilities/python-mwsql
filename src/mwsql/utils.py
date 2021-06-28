'''Utility functions used to download, open and display
 the contents of SQL dump files. Works with both .gz and
 uncompressed files.
'''

import gzip
import sys
import wget

from pathlib import Path
from urllib.error import HTTPError

# TODO: eventually will want to update the function calls to match rest of library -- e.g., file_path: string, mode: string, etc.
def open_file(file_path, mode, encoding=None):
    '''Open file and return a file handle. Works with both
    gzipped and uncompressed files.
    '''

    if 'b' in mode and encoding is not None:
        raise ValueError("Argument 'encoding' not supported in binary mode")

    if str(file_path).endswith('.gz'):
        with gzip.open(file_path, mode, encoding=encoding) as file_handle:
            yield from file_handle
    else:
        with gzip.open(file_path, mode, encoding=encoding) as file_handle:
            yield from file_handle


def head(file_path, n_lines=10, encoding='utf-8'):
    '''Display first n lines of a file. Works with both
    gzipped and uncompressed files. Defaults to 10 lines.
    '''

    if str(file_path).endswith('.gz'):
        infile = open_file(file_path, 'rt', encoding=encoding)
    else:
        infile = open_file(file_path, 'r', encoding=encoding)

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
def progress_bar(current, total, width=60):
    '''Custom progress bar for wget downloads'''

    unit = 'bytes'

    # Show file size in MB for large files
    if total >= 100000:
        MB = 1024 * 1024
        current = current / MB
        total = total / MB
        unit = 'MB'

    progress = current / total
    progress_message = (f"Progress: \
    {progress:.0%} [{current:.1f} / {total:.1f}] {unit}")
    sys.stdout.write('\r' + progress_message)
    sys.stdout.flush()


def load(db, filename):
    '''Load dump file from public dir if in PAWS, else download
    from the web. Returns a file object.
    '''

    # style: generally I only use ALL_CAPS variables when it's global so I would just change these to normal_var_names
    PAWS_ROOT_DIR = Path('/public/dumps/public/')
    DUMPS_URL = 'https://dumps.wikimedia.org/'
    subdir = Path(db, 'latest')
    extended_filename = f'{db}-latest-{filename}.sql.gz'
    file_path = Path(extended_filename)

    if PAWS_ROOT_DIR.exists():
        dump_file = Path(PAWS_ROOT_DIR, subdir, file_path)

    else:
        subdir, file_path = str(subdir), str(file_path)
        url = f'{DUMPS_URL}{subdir}/{file_path}'
        try:
            print(f'Downloading {url}')
            dump_file = wget.download(url, bar=progress_bar)
        except HTTPError:
            print('File not found')
            return None

    return dump_file
