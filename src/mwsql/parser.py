'''Helper functions used in src/dump.py'''

import re
import csv
import warnings

from typing import List


def has_sql_attribute(line: str, element_type: str) -> bool:
    '''Check whether a string contains an SQL element of the
    type specified by the argument element_type.
    '''

    line_start = {
        'database': '--',
        'insert': 'INSERT INTO',
        'create': 'CREATE TABLE',
        'primary_key': 'PRIMARY KEY',
        'col_name': '`'
    }
    contains_element = line.strip().startswith(line_start[element_type])

    if element_type == 'database':
        return (contains_element and 'Database: ' in line)

    return contains_element


def get_sql_attribute(line: str, attr_type: str):
    '''Extract SQL db/table attribute specified by
    argument attr_type from dump file.
    '''

    attr_pattern = {
        'table_name': r'`([\S]*)`',
        'col_name': r'`([\S]*)`',
        'dtype': r'` ((.)*),',
        'primary_key': r'`([\S]*)`'
    }

    try:
        if attr_type == 'database':
            attr = line.strip().partition('Database: ')[-1]

        elif attr_type in ('table_name', 'col_name', 'dtype'):
            attr = re.search(attr_pattern[attr_type], line).group(1)

        elif attr_type == 'primary_key':
            attr = (re.search(attr_pattern[attr_type], line)
                    .group(1)
                    .replace('`', '')
                    .split(',')
                    )

    except AttributeError:
        return None

    return attr


def map_dtypes(sql_dtypes):
    '''Create mapping from SQL dtypes to Python dtypes'''

    types = {}
    for key, val in sql_dtypes.items():
        if 'int' in val:
            types[key] = int
        elif any(dtype in val for dtype in ('float', 'double', 'decimal', 'numeric')):
            types[key] = float
        else:
            types[key] = str
    return types


def convert(values: List[str], dtypes, strict=False):
    '''Convert strings in list to native Python dtypes.
    With strict set to False, if any of the items in the
    list cannot be converted, it's returned unchanged,
    i.e. as a str.
    '''

    len_values = len(values)
    len_dtypes = len(dtypes)

    warn = False

    if len_values != len_dtypes:
        if not strict:
            return values

        raise ValueError('values and dtypes are not the same length')

    converted = []
    for i in range(len_dtypes):
        dtype = dtypes[i]
        val = values[i]

        try:
            conv = dtype(val)
            converted.append(conv)

        except ValueError as e:
            if values[i] == 'NULL':
                converted.append(val)
            elif not strict:
                warn = True
                converted.append(val)
            else:
                raise e('could not convert to python dtypes')

    if warn:
        warnings.warn('some rows could not be converted to Python dtypes')

    return converted


def split_tuples(line: str) -> List[str]:
    '''Split a string containing multiple SQL rows represented as
    tuples into a list of strings each representing a row.
    '''

    values = line.partition(' VALUES ')[-1].strip().replace('NULL', "'NULL'")
    # Remove `;` at the end of the last `insert into` statement
    if values[-1] == ';':
        values = values[:-1]
    records = re.split(r'\),\(', values[1:-1])  # Strip `(` and `)`

    return records


def parse(line: str,
          delimiter: str = ',',
          escape_char: str = '\\',
          quote_char: str = "'",
          doublequote: bool = False,
          strict: bool = True
          ):

    '''Parse a list of CSV-formatted strings into a
    csv reader object (generator).
    '''

    records = split_tuples(line)
    reader = csv.reader(records, delimiter=delimiter,
                                 escapechar=escape_char,
                                 quotechar=quote_char,
                                 doublequote=doublequote,
                                 strict=strict
                        )
    return reader
