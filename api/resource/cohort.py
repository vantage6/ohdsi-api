import pandas as pd

from http import HTTPStatus
from logging import getLogger

from celery.result import AsyncResult

from . import OHDSIResource

from ..task.cohort import create_all_patients_cohort

log = getLogger(__name__)


class AllPatientsCohorts(OHDSIResource):

    def post(self):
        """
        Create an all patients cohort in the OMOP CDM

        Triggering this endpoint will start the task of creating the all patients
        cohort in the OMOP CDM.
        ---
        responses:
          200:
            description: The cohort creation task was started
          500:
            description: Something went wrong

        tags: [Cohort]
        """
        try:
            result: AsyncResult = create_all_patients_cohort.delay()
        except Exception as e:
            log.exception(e)
            return {"error": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"id": result.id}, HTTPStatus.OK


class AllPatientsCohort(OHDSIResource):

    def get(self, id_):
        """
        Get the status of the all patients cohort task

        Triggering this endpoint will return the result of the
        ---
        responses:
          200:
            description: The cohort creation task was started
          500:
            description: Something went wrong

        tags: [Cohort]
        """
        result: AsyncResult = AsyncResult(id_)

        return {
            "id": id_,
            "state": result.state,
            "info": str(result.info),
            "result": str(result.result),
        }
