Release notes
=============

0.0.6
-----
*8 Oktober 2024*

- Updated the ``standard_features.sql`` to compute the ``surv`` variable. This is the
  survival time in days from the first observation to the end of the observation period
  or the death date. In case a death date is registered the censoring status is set to
  1, otherwise 0.
- Fixed the ``cohort_id`` filter in the ``standard_features.sql`` query. This was
  previously not working correctly.


0.0.5
-----

- Added the  ``OMOP_RESULT_SCHEMA`` environment variable to the ``OHDSITask`` class.
  This can be used to specify the schema where for example the cohorts are stored.
- Added the ``/all-patients-cohorts`` and ``/all-patients-cohorts/<cohort_id>``
  endpoints to manage the *allPatients* cohort which can be used to retrieve data from
  all patients. In this case users are not able to supply their own OHDSI cohort
  definitions.
- Added the ``/query-standard-features`` and ``/query-standard-feature/<string:id_>``
  endpoints to query the standard features that are available in the OMOP CDM. Note
  that this endpoint returns a single record per patient by selecting the first
  observation.

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