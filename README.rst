XML Schema Definition (XSD) for an Equipment Register.

For background information about XSD, please see the following overview
provided by the `World Wide Web Consortium <https://www.w3.org/>`_.

1. `XML Schema Part 0: Primer <https://www.w3.org/TR/xmlschema-0/>`_
2. `XML Schema Part 1: Structures <https://www.w3.org/TR/xmlschema-1/>`_
3. `XML Schema Part 2: Datatypes <https://www.w3.org/TR/xmlschema-2/>`_

Developer Guide
===============
Python is required to run the tests and to build the documentation.

To install the dependencies run

.. code-block:: console

   pip install pytest lxml

Testing
-------
To run the tests, execute the following command from the root directory
of the repository

.. code-block:: console

   pytest

Documentation
-------------
To build the documentation, run

.. code-block:: console

   python build_docs.py

See the ``docs/README.rst`` file for information about the build process.
