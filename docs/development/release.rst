Release
=======
To create a release simply create a tag on the ``main`` branch in the following format:

.. code-block:: bash

    git tag -a 0.1.0 -m "Release 0.1.0"
    git push origin 0.1.0

Note that the version number should be in the format ``major.minor.patch``. The pipeline
currently does not support pre or post releases.

This releases the package to our container registry. It will tag is with the version
number and ``latest``. The ``latest`` tag will always point to the latest release.