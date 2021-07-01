"""Helper functions used in src/dump.py"""

import re
import csv
import warnings

from typing import Any, Dict, List, Iterator, Optional


def has_sql_attribute(line: str, element_type: str) -> bool:
    """Check whether a string contains an SQL element of the
    type specified by the argument element_type.
    """

    # FYI: no need to update this because I think it's nice and simple but if you were trying to
    # expand it to more use cases and finding the rules to get more complex, you would likely want to consider
    # a regex for each like in get_sql_attribute.
    # e.g., something like (with the caveat that I am not good at regexes): re.match('(^--).*(Database: )', line)
    line_start = {
        "database": "--",
        "insert": "INSERT INTO",
        "create": "CREATE TABLE",
        "primary_key": "PRIMARY KEY",
        "col_name": "`",
    }
    contains_element = line.strip().startswith(line_start[element_type])

    if element_type == "database":
        return contains_element and "Database: " in line

    return contains_element


def get_sql_attribute(line: str, attr_type: str) -> Optional[str]:
    """Extract SQL db/table attribute specified by
    argument attr_type from dump file.
    """

    attr_pattern = {
        "table_name": r"`([\S]*)`",
        "col_name": r"`([\S]*)`",
        "dtype": r"` ((.)*),",
        "primary_key": r"`([\S]*)`",
    }

    attr: Optional[str] = None

    try:
        if attr_type == "database":
            attr = line.strip().partition("Database: ")[-1]

        elif attr_type in ("table_name", "col_name", "dtype"):
            attr = re.search(attr_pattern[attr_type], line).group(1)  # type: ignore

        elif attr_type == "primary_key":
            attr = (
                re.search(attr_pattern[attr_type], line)
                .group(1)  # type: ignore
                .replace("`", "")
                .split(",")
            )

    except AttributeError:
        return None

    # probably define attr as None before the try clause. right now if not of the if-else clauses matched, would throw a weird error
    return attr


# I don't know much about the intricacies of types but I like this -- good and simple!
def map_dtypes(sql_dtypes: Dict[str, str]) -> Dict[str, type]:
    """Create mapping from SQL dtypes to Python dtypes"""

    types: Dict[str, type] = {}
    for key, val in sql_dtypes.items():
        if "int" in val:
            types[key] = int
        elif any(
            dtype in val for dtype in ("float", "double", "decimal", "numeric")
        ):
            types[key] = float
        else:
            types[key] = str
    return types


def convert(
    values: List[str], dtypes: List[type], strict: bool = False
) -> List[Any]:
    """Convert strings in list to native Python dtypes.
    With strict set to False, if any of the items in the
    list cannot be converted, it's returned unchanged,
    i.e. as a str.
    """

    len_values = len(values)
    len_dtypes = len(dtypes)

    warn = False

    if len_values != len_dtypes:
        if not strict:
            return values

        raise ValueError("values and dtypes are not the same length")

    converted = []
    for i in range(len_dtypes):
        dtype = dtypes[i]
        val = values[i]

        try:
            conv = dtype(val)
            converted.append(conv)

        except ValueError as e:
            if values[i] == "":
                # why not convert to None?
                converted.append(val)
            elif not strict:
                warn = True
                converted.append(val)
            else:
                # my PyCharm installation doesn't like this and things it won't work FYI. I haven't tested it though.
                # You're right - I've changed this now.
                print(f"ValueError: {e}")

    if warn:
        # low priority: perhaps include the values too? or problematic value?
        warnings.warn("some rows could not be converted to Python dtypes")

    return converted


def split_tuples(line: str) -> List[str]:
    """Split a string containing multiple SQL rows represented as
    tuples into a list of strings each representing a row.
    """

    # I think the NULL replacement might need some tweaking. The challenge is two-fold:
    # * making NULL into something that doesn't break the parser -- that's easy, either add quotes like you do or replace with None
    # > I have opted for replacing NULL with the empty string when it's used
    # to denote missing values (i.e. not part of some other string). The reason
    # is that `None` is somewhat specific to pure Python while Pandas, Numpy, R, CSV, and others recognize the empty string as a missing value and sub it with their own null equivalent (NaN, NA, <na>, ...)
    # * not making this replacement when e.g., NULL is just part of a real value like a page title as happens in Commons sometimes
    # For the latter, I think you might need to a regex that only does the replacement when it sees any of the following
    # which in theory should capture all the ways that NULL shows up as a full field value:
    # * ,NULL,
    # * (NULL,
    # * ,NULL)
    # > Good suggestion - I have implemented this regex.
    tuples = line.partition(" VALUES ")[-1].strip()
    # Sub NULL with empty string
    pattern = r"(?<=[,(])NULL(?=[,)])"
    values = re.sub(pattern, "", tuples)
    # Remove `;` at the end of the last `insert into` statement
    if values[-1] == ";":
        values = values[:-1]
    records = re.split(r"\),\(", values[1:-1])  # Strip `(` and `)`

    return records


def parse(
    line: str,
    delimiter: str = ",",
    escape_char: str = "\\",
    quote_char: str = "'",
    doublequote: bool = False,
    strict: bool = True,
) -> Iterator[List[str]]:

    """Parse a list of CSV-formatted strings into a
    csv reader object (generator).
    """

    records = split_tuples(line)
    reader = csv.reader(
        records,
        delimiter=delimiter,
        escapechar=escape_char,
        quotechar=quote_char,
        doublequote=doublequote,
        strict=strict,
    )
    return reader
