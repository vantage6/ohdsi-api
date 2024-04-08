.. ohdsi-api documentation master file, created by
   sphinx-quickstart on Thu Nov 16 08:51:42 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OHDSI API
=========
This API designed to retrieve data from an OMOP data source through an HTTP connection. It can also be used to
execute OHDSI community tools such as
`CohortDiagnostics <https://ohdsi.github.io/CohortDiagnostics/>`_ and retrieve their
results.

This project has been created for the `IDEA4RC project <https://www.idea4rc.eu/>`_. It
allows to connects the `vantage6 <https://vantage6.ai>`_ platform to an OMOP data
source. It uses `python-ohdsi <https://python-ohdsi.readthedocs.org>`_, a package also
to created in this project context to interface with the OMOP data source.

.. toctree::
    :maxdepth: 2

    user/quickstart
    user/endpoints

.. toctree::
   :maxdepth: 2
   :caption: Development

   development/documentation
   development/release
   development/release_notes



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
