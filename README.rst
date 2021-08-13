Overview
========

``mwsql`` provides utilities for working with Wikimedia SQL dump files.
It supports Python 3.6 and later versions.

``mwsql`` abstracts the messiness of working with SQL dump files.
Each Wikimedia SQL dump file contains one database table.
The most common use case for ``mwsql`` is to convert this table into a more user-friendly Python ``Dump class`` instance.
This lets you access the table's metadata (db names, field names, data types, etc.) as attributes, and its content – the table rows – as a generator, which enables processing of larger-than-memory datasets due to the inherent lazy/delayed execution of Python generators.

``mwsql`` also provides a method to convert SQL dump files into CSV.
You can find more information on how to use ``mwsql`` in the `usage examples`_.


Installation
------------

You can install ``mwsql`` with ``pip``:

.. code-block:: bash

   $ pip install mwsql


Basic Usage
-----------

.. code-block:: pycon

   >>> from mwsql import Dump
   >>> dump = Dump.from_file('simplewiki-latest-change_tag_def.sql.gz')
   >>> dump.head(5)
   ['ctd_id', 'ctd_name', 'ctd_user_defined', 'ctd_count']
   ['1', 'mw-replace', '0', '10453']
   ['2', 'visualeditor', '0', '309141']
   ['3', 'mw-undo', '0', '59767']
   ['4', 'mw-rollback', '0', '71585']
   ['5', 'mobile edit', '0', '234682']
   >>> dump.dtypes
   {'ctd_id': int, 'ctd_name': str, 'ctd_user_defined': int, 'ctd_count': int}
   >>> rows = dump.rows(convert_dtypes=True)
   >>> next(rows)
   [1, 'mw-replace', 0, 10453]


Known Issues
------------


Encoding errors
~~~~~~~~~~~~~~~

Wikimedia SQL dumps use utf-8 encoding.
Unfortunately, some fields can contain non-recognized characters, raising an encoding error when attempting to parse the dump file.
If this happens while reading in the file, it's recommended to try again using a different encoding. ``latin-1`` will sometimes solve the problem; if not, you're encouraged to try with other encodings.
If iterating over the rows throws an encoding error, you can try changing the encoding.
In this case, you don't need to recreate the dump – just pass in a new encoding via the ``dump.encoding`` attribute.


Parsing errors
~~~~~~~~~~~~~~

Some Wikimedia SQL dumps contain string-type fields that are sometimes not correctly parsed, resulting in fields being split up into several parts.
This is more likely to happen when parsing dumps containing file names from Wikimedia Commons or containing external links with many query parameters.
If you're parsing any of the other dumps, you're unlikely to run into this issue.

In most cases, this issue affects a relatively very small proportion of the total rows parsed.
For instance, Wikimedia Commons ``page`` dump contains approximately 99 million entries, out of which ~13.000 are incorrectly parsed.
Wikimedia Commons ``page links`` on the other hand, contains ~760M records, and only 20 are wrongly parsed.

This issue is most commonly caused by the parser mistaking a single quote (or apostrophe, as they're identical) within a string for the single quote that marks the end of said string.
There's currently no known workaround other than manually removing the rows that contain more fields than expected, or if they are relatively few, manually merging the split fields.

Future versions of ``mwsql`` will improve the parser to correctly identify when single quotes should be treated as string delimiters and when they should be escaped. For now, it's essential to be aware that this problem exists.


Project information
-------------------

``mwsql`` is released under the `MIT license`_.
You can find the complete documentation at `Read the Docs`_. If you run into bugs, you can file them in our `issue tracker`_.
Have ideas on how to make ``mwsql`` better?
Contributions are most welcome – we have put together a guide on how to `get started`_.


.. _`MIT license`: https://choosealicense.com/licenses/mit/
.. _`Read the Docs`: https://mwsql.readthedocs.io/en/latest/
.. _`usage examples`: https://mwsql.readthedocs.io/en/latest/examples.html
.. _`get started`: https://mwsql.readthedocs.io/en/latest/contributing.html
.. _`issue tracker`: https://github.com/blancadesal/mwsql/issues
