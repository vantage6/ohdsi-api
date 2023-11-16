Documentation
=============

Local build
-----------

To build the documentation locally, you need to install the following packages:

.. code-block:: bash

    pip install -r docs/requirements.txt
    pip install sphinx sphinx-autobuild

Then you can build the documentation by running:

.. code-block:: bash

    sphinx-autobuild docs docs/_build/html


ReadTheDocs
-----------
On every push on the main branch the documentation is automatically built and deployed
on `ReadTheDocs <https://readthedocs.org/projects/ohdsi-api/>`_.