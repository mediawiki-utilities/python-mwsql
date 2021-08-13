Usage examples
==============


Loading a dump file
-------------------

`Wikimedia SQL dump files`_ are publicly available and can be downloaded from the web.
They can also be directly accessed through Wikimedia environments like PAWS or Toolforge.
``mwsql`` includes a load utility for easy (down)loading of dump files – All you need to know is which file you need.
For this example, we want to download the latest ``pages`` dump from the Simple English Wikipedia.
If we go to https://dumps.wikimedia.org/simplewiki/latest/, we see that this file is called ``simplewiki-latest-page.sql.gz``.
Instead of manually downloading it, we can do the following:

.. code-block:: python

   >>> from mwsql import load
   >>> dump_file = load('simplewiki', 'page')

If you *are not* in a Wikimedia hosted environment, the file will now be downloaded to your current working directory, and you will see a progress bar:

.. code-block:: python

   >>> dump_file = load('simplewiki', 'page')
   Downloading https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz
   Progress:     92% [19.0 / 20.7] MB

If you *are* in a Wikimedia hosted environment, the file is already available to you and does not need downloading. The syntax is the same, however:

.. code-block:: python

   >>> dump_file = load('simplewiki', 'page')

In both cases, ``dump_file`` will be a PathObject that points to the file.


Loading a dump file from a different date
-----------------------------------------

The default behavior of the ``load`` function is to load the file from the latest dump. If you want to use a file from an earlier date, you can specify this by passing the date as a string to the ``date`` parameter:

.. code-block:: python

   >>> dump_file = load('simplewiki', 'page', '20210720')


Peeking at a dump file
----------------------

Before diving into the data contained in the dump, you may want to look at its raw contents. You can do so by using the ``head`` function:

.. code-block:: python

   >>> from mwsql import head
   >>> head(dump_file)
   -- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)
   --
   -- Host: 10.64.32.82    Database: simplewiki
   -- ------------------------------------------------------
   -- Server version   10.4.19-MariaDB-log

   /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
   /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
   /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
   /*!40101 SET NAMES utf8mb4 */;


By default, the ``head`` function prints the first 10 lines.
This can be changed to anything you want by specifying it in the function call:

.. code-block:: python

   >>> from mwsql import head
   >>> head(dump_file, 5)
   -- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)
   --
   -- Host: 10.64.32.82    Database: simplewiki
   -- ------------------------------------------------------
   -- Server version   10.4.19-MariaDB-log


Creating a dump object from file
--------------------------------

The main use of the ``mwsql`` library is to parse an SQL dump file and turn it into an object that is easier to work with.

.. code-block:: python

   >>> from mwsql import Dump
   >>> dump = Dump.from_file(file_path)

The file that ``file_path`` refers to can be either a ``.sql`` or a ``.sql.gz`` file. Now that we have instantiated a Dump object, we can access its attributes:

.. code-block:: python

   >>> dump = Dump.from_file('simplewiki-latest-page.sql.gz')
   >>> dump
   Dump(database=simplewiki, name=page, size=21654225)
   >>> dump.col_names
   ['page_id', 'page_namespace', 'page_title', 'page_restrictions', 'page_is_redirect', 'page_is_new', 'page_random', 'page_touched', 'page_links_updated', 'page_latest', 'page_len', 'page_content_model', 'page_lang']
   >>> dump.encoding
   'utf-8'

There are other attributes a well, such as ``dtypes`` or ``primary_key``.
See the `Module Reference`_ for a complete list.


Displaying the rows
-------------------

The most interesting part of an SQL table is arguably its entries (rows.)
We can take a look at them by using the ``head`` method.
Note that this is different than the ``head`` *function* we used to peek at a file *before* we turned it into a Dump object.

.. code-block:: python

   >>> dump_file = load('simplewiki', 'change_tag_def')
   >>> dump = Dump.from_file(dump_file)
   >>> dump
   Dump(database=simplewiki, name=change_tag_def, size=2133)
   >>> dump.head()
   ['ctd_id', 'ctd_name', 'ctd_user_defined', 'ctd_count']
   ['1', 'mw-replace', '0', '10453']
   ['2', 'visualeditor', '0', '309141']
   ['3', 'mw-undo', '0', '59767']
   ['4', 'mw-rollback', '0', '71585']
   ['5', 'mobile edit', '0', '234682']
   ['6', 'mobile web edit', '0', '227115']
   ['7', 'very short new article', '0', '28794']
   ['8', 'visualeditor-wikitext', '0', '20529']
   ['9', 'mw-new-redirect', '0', '30423']
   ['10', 'visualeditor-switched', '0', '18009']


By default, the ``head`` method prints the ``col_names``, followed by the first ten rows. You can change this by passing how many rows you'd like to see as a parameter:

.. code-block:: python

   >>> dump.head(3)
   ['ctd_id', 'ctd_name', 'ctd_user_defined', 'ctd_count']
   ['1', 'mw-replace', '0', '10453']
   ['2', 'visualeditor', '0', '309141']
   ['3', 'mw-undo', '0', '59767']


Iterating over rows
-------------------

If we want to access the rows, all we need to do is create a generator object by using the Dump's ``rows`` method.

.. code-block:: python

   >>> dump_file = load('simplewiki', 'change_tag_def')
   >>> dump = Dump.from_file(dump_file)
   >>> dump
   Dump(database=simplewiki, name=change_tag_def, size=2133)
   >>> rows = dump.rows()
   >>> for _ in range(5):
           print(next(rows))
   ['1', 'mw-replace', '0', '10453']
   ['2', 'visualeditor', '0', '309141']
   ['3', 'mw-undo', '0', '59767']
   ['4', 'mw-rollback', '0', '71585']
   ['5', 'mobile edit', '0', '234682']


Converting to Python dtypes
---------------------------

Note that in the above example, *all* values were printed as strings – even those that seem to be of a different dtype.
We can tell the ``rows`` method that we would like to convert numeric types to int or float by setting the ``convert_dtypes`` parameter to ``true``:

.. code-block:: python

   >>> rows = dump.rows(convert_dtypes=True)
   >>> for _ in range(5):
           print(next(rows))
   [1, 'mw-replace', 0, 10453]
   [2, 'visualeditor', 0, 309141]
   [3, 'mw-undo', 0, 59767]
   [4, 'mw-rollback', 0, 71585]
   [5, 'mobile edit', 0, 234682]


Exporting as CSV
----------------

You can export the dump as a CSV file by using the ``to_csv`` method and specifying a ``file path`` for the output file:

.. code-block:: python

   >>> dump_file = Dump.from_file(some_file)
   >>> dump.to_csv('some_folder/outfile.csv')

While this may take some time for larger files, you don't risk running out of memory as neither the input nor the output file is ever loaded into RAM in one big chunk.


.. _`Wikimedia SQL dump files`: https://dumps.wikimedia.org/
.. _`Module Reference`: https://mwsql.readthedocs.io/en/latest/module-reference.html
