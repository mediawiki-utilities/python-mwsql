How To Contribute
=================

First of all, thank you for considering contributing to ``mwsql``!
The intent of this document is to help get you started.
Don't be afraid to reach out with questions – no matter how "silly.”
Just open a PR whether you have made any significant changes or not, and we'll try to help. You can also open an issue to discuss any changes you want to make before you start.


Basic Guidelines
----------------

- Contributions of any size are welcome! Fixed a typo?
  Changed a docstring? No contribution is too small.
- Try to limit each pull request to *one* change only.
- *Always* add tests and docs for your code.
- Make sure your proposed changes pass our CI_.
  Until it's green, you risk not getting any feedback on it.
- Once you've addressed review feedback, make sure to bump the pull request with a comment so we know you're done.


Local Dev Environment
---------------------

To start, create a `virtual environment <https://virtualenv.pypa.io/>`_ and activate it.
If you don't already have a preferred way of doing this, you can take a look at some commonly used tools: `pew <https://github.com/berdario/pew>`_, `virtualfish <https://virtualfish.readthedocs.io/>`_, and `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/>`_.

Next, get an up to date checkout of the ``mwsql`` repository via ``SSH``:

.. code-block:: bash

    $ git clone git@github.com:blancadesal/mwsql.git

or if you want to use git via ``https``:

.. code-block:: bash

    $ git clone https://github.com/blancadesal/mwsql.git

Change into the newly created directory and install an editable version of ``mwsql``:

.. code-block:: bash

    $ cd mwsql
    $ pip install -e .

pip will install all the necessary dependencies for you, no need to install from a separate ``requirements.txt`` file.

Dev dependencies
----------------

The only dependency you *really* need to install is tox_. It will handle everyhing else for you,
including running tests, formatting and linting through pre-commit, and building and serving the latest version of the documentation. Below are a few examples of how to run tox:

.. code-block:: bash

    $ tox
    # This will run the full pytest suite, as well as pre-commit.
    # These are the same tests that are run by the CI

    $ tox -e pre-commit
    # This will run the pre-commit linting and formatting checks

    $ tox -e docs
    # This will run the documentation build process

    $ tox -e serve-docs
    # Live-serve docs with Sphinx autobuild


Code style
----------

- We use flake8_ to enforce `PEP 8`_ conventions, isort_ to sort our imports, and we use the black_ formatter with a line length of 88 characters.
  Static typing is enforced using mypy_.
  Code that does not follow these conventions won't pass our CI.
  These tools are configured in either ``tox.ini`` or ``pyproject.toml``.
- Make sure your docstrings are formatted using the `Sphinx-style format`_ like in the example below:

.. code-block:: python

    def add_one(number: int) -> int:
        """
        Add one to a number.

        :param number: A very important parameter.
        :type number: int
        :rtype: int
        """

- As long as you run the tox_ suite before submitting a PR, you should be fine.
  Tox runs all the tools above by calling pre-commit_. It also runs the whole pytest_ suite (see Tests below) across all supported Python versions, the same as the CI workflow.

.. code-block:: bash

  $ tox

- See the section above how to run pre-commit on its own via tox


Tests
-----

- We use pytest_ for testing. For the sake of consistency, write your asserts as ``actual == expected``:

.. code-block:: python

    def test_add_one():
       assert func(2) == 3
       assert func(4) == 5

- You can run the test suite either through tox or directly with pytest:

.. code-block:: bash

   $ python -m pytest


Docs
----

- Use `semantic newlines`_ in ``.rst`` files (reStructuredText_ files):

.. code-block:: rst

    This is a sentence.
    This is another sentence.

- If you start a new section, add two blank lines before and one blank line after the header, except if two headers follow immediately after each other:

.. code-block:: rst

    Last line of previous section.


    Header of New Top Section
    -------------------------

    Header of New Section
    ^^^^^^^^^^^^^^^^^^^^^

    First line of new section.

- If you add a new feature, include one or more usage examples in ``examples.rst``.


.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/backward-compatibility.html
.. _tox: https://tox.readthedocs.io/
.. _reStructuredText: https://www.sphinx-doc.org/en/stable/usage/
.. _`Sphinx-style format`: https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html#the-sphinx-docstring-format
.. _semantic newlines: https://rhodesmill.org/brandon/2012/one-sentence-per-line/restructuredtext/basics.html
.. _CI: https://github.com/blancadesal/mwsql/actions
.. _black: https://github.com/psf/black
.. _pre-commit: https://pre-commit.com/
.. _isort: https://github.com/PyCQA/isort
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _mypy: https://mypy.readthedocs.io/en/stable/
.. _pytest: https://docs.pytest.org/en/6.2.x/
