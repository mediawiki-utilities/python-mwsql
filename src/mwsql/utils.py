'''Helper functions used in src/mwsql.py'''

import csv
import gzip
import re
import sys

from typing import List

# Allow long field names
csv.field_size_limit(sys.maxsize)


def head(file_path, n_lines=10):
    '''Display top of compressed file, similar to `zcat | head` UNIX utility'''

    with gzip.open(file_path, 'rt', encoding='utf-8') as infile:
        for line in infile:
            print(line.strip())
            n_lines -= 1
            if n_lines == 0:
                break


# mwsql helper functions
def is_insert_statement(line: str) -> bool:
    '''Check whether a string is an SQL `insert into` statement.'''

    return line.startswith('INSERT INTO')


def is_create_statement(line: str) -> bool:
    '''Check whether a string is an SQL `create table` statement.'''

    return line.startswith('CREATE TABLE')


def get_table_name(line: str) -> str:
    '''Extract SQL table name from string'''

    table_name_pattern = r'`([\S]*)`'
    table_name = re.search(table_name_pattern, line).group(1)
    return table_name


def has_col_name(line: str) -> bool:
    '''Check whether a string contains an SQL column name'''

    return line.strip().startswith('`')


def get_col_name(line: str) -> str:
    '''Extract SQL column names and data types from string'''

    col_name_pattern = r'`([\S]*)`'
    col_name = re.search(col_name_pattern, line).group(1)

    # I was going to suggest trying to map SQL dtypes to numpy or native dtypes in Python
    # but then I feel like most libraries like Pandas auto-detect and do this for you
    # so probably not necessary.
    col_dtype_pattern = r'` ((.)*),'
    col_dtype = re.search(col_dtype_pattern, line).group(1)

    return col_name, col_dtype


def has_primary_key(line: str) -> str:
    '''Check whether a string contains an SQL primary key'''

    return line.strip().startswith('PRIMARY KEY')


def get_primary_key(line: str) -> str:
    '''Extract SQL table primary key from string'''

    pattern = r'`([\S]*)`'
    primary_key = re.search(pattern, line).group(1).replace('`', '').split(',')

    return primary_key


def parse_records(records: List[str]):
    '''Parse an SQL `insert into` statement into separate records
    (also called values, rows, entries...) and return as a csv.reader object.
    '''

    reader = csv.reader(records, delimiter=',',
                                 doublequote=False,
                                 escapechar='\\',
                                 quotechar="'",
                                 strict=True
                        )
    return reader


def get_records(line: str) -> List[str]:
    '''Split a string containing multiple SQL value tuples into a list
    where each element is a csv reader object representing the tuple.
    '''

    values = line.partition(' VALUES ')[-1].strip().replace('NULL', "''")
    # Remove `;` at the end of the last `insert into` statement
    if values[-1] == ';':
        values = values[:-1]
    # Maybe it's too much of an edge case to worry about, but technically if "),(" appeared in a data tuple -- e.g., as part of a page title --
    # it would be split falsely. I wonder if there is some lightweight way to enforce the # of expected columns and intelligently recombine broken tuples?
    records = re.split(r'\),\(', values[1:-1])  # Strip `(` and `)`

    return parse_records(records)
