Release notes
=============

0.0.5
-----

- Added the  ``OMOP_RESULT_SCHEMA`` environment variable to the ``OHDSITask`` class.
  This can be used to specify the schema where for example the cohorts are stored.
- Added the ``/cohorts`` endpoint to return the create an *allPatients* cohort which
  can be used to retrieve data from all patients. In this case users are not able
  to supply their own OHDSI cohort definitions.

0.0.4
-----
*5 December 2023*

- The endpoints ``/celery`` and ``/count`` now have settable schema's. These should be
  defined in the environment variable ``OMOP_CDM_SCHEMA``. There is no default, so
  make sure to specify this in the environment file.

0.0.3
-----
*30 November 2023*

- Added ``/version`` endpoint to return the version of the application.
- Added the celery backend status to the ``/health`` endpoint.
- Minor stability improvements.


0.0.2
-----
*16 November 2023*

- Added ``/error`` endpoint to test error handling.
-
- Added ``/count`` endpoint to count the number of observations in the person table.
  This uses a direct SQL connection (not using celery).
- Added ``/celery``, ``/result/<task_id>`` endpoints. This allows testing the celery
  workflow.


0.0.1
-----
*01 November 2023*

- First release, only contains the ``/health`` endpoint.