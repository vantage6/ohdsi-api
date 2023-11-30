Release notes
=============

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