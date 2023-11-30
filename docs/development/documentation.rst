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

Note that in order to update the OAS documentation, you need to run the following
command from the root directory:

.. code-block:: bash

    flask --app api generate-api-schema -f ./docs/user/api-schema.json

.. note::

    I made a first attempt of also generating the documentation from on the fly on
    readthedocs, however this was challenging due to the side effects of the imports
    of ``rpy2``.