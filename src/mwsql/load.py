'''Utilities for easy loading of dump files from
PAWS or from the web'''

import sys
import wget

from pathlib import Path
from urllib.error import HTTPError
from mwsql import Dump


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
    progress_message = f"Progress: {progress:.0%} [{current:.1f} / {total:.1f}] {unit}"
    sys.stdout.write('\r' + progress_message)
    sys.stdout.flush()


def load(db, filename):
    '''Load dump file from public dir if in PAWS, else download
    from the web. Returns a Dump object.
    '''

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

    return Dump.from_file(dump_file)
