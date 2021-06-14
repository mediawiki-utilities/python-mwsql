'''Helper functions used in src/dump.py'''

import gzip
import re
import sys


from typing import List


def head(file_path, n_lines=10):
    '''Display top of compressed file, similar to `zcat | head` in GNU'''

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


def parse_sql_stmt(line: str) -> List[List[str]]:
    '''Parse an SQL INSERT INTO statement into a list
    of lists representing the rows in the table.
    '''

    out = []
    tup = []
    field = []

    in_tuple = False
    in_quote = False

    for i in range(1, len(line) -1):
        prev = line[i-1]
        curr = line[i]

        if in_tuple and curr not in "()',":
            field.append(curr)

        elif curr == '(':
            if not in_quote:
                in_tuple = True
            elif in_quote:
                field.append(curr)

        elif curr == ')':
            if not in_quote:
                in_tuple = False
            else:
                field.append(curr)

        elif curr == "'":
            if not in_quote:
                in_quote = True
            elif in_quote:
                if prev != '/':
                    in_quote = False

        elif curr == ',':
            if not in_quote and not in_tuple:
                tup.append(''.join(field))
                out.append(tup)
                field = []
                tup = []
            elif in_quote:
                field.append(curr)
            elif in_tuple and not in_quote:
                tup.append(''.join(field))
                field = []

    tup.append(''.join(field))
    out.append(tup)
    return out

