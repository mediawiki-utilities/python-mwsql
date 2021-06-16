'''Helper functions used in src/dump.py'''

import gzip
import re
import csv
import warnings

from typing import List


def is_sql_statement(line: str, statement_type: str) -> bool:
    '''Check whether a string is an SQL statement'''

    sql_stmts = {
        'insert': 'INSERT INTO',
        'create': 'CREATE TABLE',
        'primary_key': 'PRIMARY KEY',
        'col_name': '`'
        }

    stmt = sql_stmts[statement_type]

    return line.strip().startswith(stmt)


def get_sql_attribute(line: str, attr_type: str):

    attr_pattern = {
        'table_name': r'`([\S]*)`',
        'col_name': r'`([\S]*)`',
        'dtype': r'` ((.)*),',
        'primary_key': r'`([\S]*)`'
    }

    try:
        if attr_type in ('table_name', 'col_name', 'dtype'):
            attr = re.search(attr_pattern[attr_type], line).group(1)

        elif attr_type == 'primary_key':
            attr = re.search(attr_pattern[attr_type], line).group(1).replace('`', '').split(',')

    except AttributeError:
        return None

    return attr


def map_dtypes(sql_dtypes):
    '''Create mapping from SQL dtypes to Python dtypes'''

    types = {}
    for k, v in sql_dtypes.items():
        if 'int' in v:
            types[k] = int
        elif any(t in v for t in ('float', 'double', 'decimal', 'numeric')):
            types[k] = float
        else:
            types[k] = str
    return types


def convert(values, dtypes, strict=False):
    '''Convert output of SQL parser to native Python dtypes'''

    len_values = len(values)
    len_dtypes = len(dtypes)
    if len_values != len_dtypes:
        raise ValueError('lenghts of iterables are different')

    try:
        converted = [dtypes[i](values[i]) for i in range(len_dtypes)]
        return converted
    except ValueError:
        if not strict:
            warnings.warn('could not convert to python dtypes')
            return values
        else:
            print('could not convert to python dtypes:', values)


def split_tuples(line: str) -> List[str]:
    '''Split a string containing multiple SQL rows represented as
    tuples into a list of strings each representing a row.
    '''

    values = line.partition(' VALUES ')[-1].strip().replace('NULL', "''")
    # Remove `;` at the end of the last `insert into` statement
    if values[-1] == ';':
        values = values[:-1]
    records = re.split(r'\),\(', values[1:-1])  # Strip `(` and `)`

    return records


def parse(line: str, delimiter: str =',',
                     escape_char: str ='\\',
                     quote_char: str ="'",
                     doublequote: bool=False,
                     strict: bool=True
         ):

    '''Parse a list of CSV-formatted strings into a
    csv reader object (generator).
    '''

    records = split_tuples(line)
    reader = csv.reader(records, delimiter=delimiter,
                                 escapechar=escape_char,
                                 quotechar=quote_char,
                                 doublequote=doublequote,
                                 strict=True
                        )
    return reader