'''Utilities for easy loading of dump files from
PAWS or from the web'''

import os
import sys
import wget

from mwsql import Dump
from urllib.error import HTTPError


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


def get_source(db, filename):
    '''Determine where to get the dump files from depending
    on if the user's environment is PAWS or local.
    '''

    # If in PAWS, set dir
    # NOTE: I think this covers Toolforge too thankfully!
    if os.path.exists('/public/dumps/public/'):
        prefix = '/public/dumps/public/'
        download = False

    # If in other environment, set url
    else:
        prefix = 'https://dumps.wikimedia.org/'
        download = True

    # TODO: probably more robust to use os.path.join() here for all the pieces
    source = f'{prefix}{db}/latest/{db}-latest-{filename}.sql.gz'
    return source, download


def load(db, filename):
    '''Load dump file from public dir if in PAWS, else download
    from the web if the file doesn't already exist in the user's
    current working directory
    '''

    source, download = get_source(db, filename)

    if download:
        try:
            print(f'Downloading {source}')
            cwd = os.getcwd()
            file = wget.download(source, bar=progress_bar)
            file_path = os.path.join(cwd, file)

        except HTTPError:
            print('File not found')
            return None

    else:
        file_path = source

    try:
        dump = Dump.from_file(file_path)
        return dump

    # TODO: eventually will want to make the error catching more explicit. clearer code and otherwise keyboard interrupts won't actually stop the program
    except:
        print("Couldn't create dump")
        return None
