'''A set of utilities for processing MediaWiki SQL dump data'''

__version__ = '0.1.0'

import os
import gzip

from mwsql import utils


class Dump:
    '''Class for parsing an SQL dump file and processing its contents'''

    def __init__(self, table_name, col_names, col_dtypes, primary_key, source_file):

        self.name = table_name
        self.col_names = col_names
        self.dtypes = col_dtypes
        self.primary_key = primary_key
        self.size = os.path.getsize(source_file)
        self._source_file = source_file

    def __iter__(self):
        return self.rows

    @property
    def rows(self):
        '''Create a generator object from the rows'''

        with gzip.open(self._source_file, 'rt', encoding='ISO-8859-1') as infile:
            for line in infile:
                if utils.is_insert_statement(line):
                    rows = utils.get_records(line)
                    for row in rows:
                        yield row

    @classmethod
    def from_file(cls, file_path):
        '''Initialize mwsql object from dump file'''

        source_file = file_path
        table_name = None
        primary_key = None
        col_names = []
        col_dtypes = {}

        with gzip.open(file_path, 'rt', encoding='ISO-8859-1') as infile:
            for line in infile:
                if utils.is_insert_statement(line):
                    # All metadata is extracted so we return it
                    return cls(table_name, col_names, col_dtypes, primary_key, source_file)
                if utils.is_create_statement(line):
                    table_name = utils.get_table_name(line)
                elif utils.has_col_name(line):
                    col_name, dtype = utils.get_col_name(line)
                    col_names.append(col_name)
                    col_dtypes[col_name] = dtype
                elif utils.has_primary_key(line):
                    primary_key = utils.get_primary_key(line)
        return None

    def to_csv(self, file_path):
        '''Convert mwsql object into CSV file'''
        # creates the specified outfile if it doesn't exist
        # raises an error if the outfile already exist to avoid overwriting

        raise NotImplementedError

    def head(self, n_lines=5):
        '''Display first n rows'''

        rows = self.rows
        print(self.col_names)
        return [next(rows) for _ in range(n_lines)]
