Installation Guide
#####################

Latest Release
====================

Pypotage installation is pretty straightforward. You can install the latest release using pip:

.. code-block:: bash

   python -m pip install -U pypotage

After the installation, you can start using the package by importing it in your Python code:

.. code-block:: python3

   import pypotage

That's all you need to do to install the latest version of the package. You can now start using it on your own or follow the :doc:`basic_usage` guide to get started.


Development Version
====================

In case you want to check out the latest features or wanna contribute to the project,
you can install the latest development version from the GitHub repository:

.. code-block:: bash

   git clone https://github.com/pavalso/potage.git
   cd potage
   python -m pip install -U .

Development
====================

In case you want to contribute to this proyect you'll need to install the required dependencies for it:

.. code-block:: bash

   python -m pip install --editable -U .[dev]

This will install all the dependencies required for:

- Testing
- Documentation

You can also install the required dependencies for each section:

.. code-block:: bash

   python -m pip install --editable -U .[test]

Or for documentation

.. code-block:: bash

   python -m pip install --editable -U .[doc]

Tests
====================

Tests are written using the `pytest` framework. First you will need to install the required dependencies to use it:

.. code-block:: bash

   python -m pip install -r ./tests/requirements.txt

After that, you can run the tests using the following command:

.. code-block:: bash

   python -m pytest tests/

In case you want to get the coverage report, you can use the following command:

.. code-block:: bash

   python -m pytest --cov=src/ tests/
