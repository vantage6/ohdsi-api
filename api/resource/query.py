import pandas as pd

from http import HTTPStatus
from logging import getLogger

from celery.result import AsyncResult

from . import OHDSIResource

from ..task.query import query_standard_features

log = getLogger(__name__)


class QueryStandardFeatures(OHDSIResource):

    def post(self):
        """
        Create a task that

        Triggering this endpoint will create a task to retrieve the standard features
        of the OMOP database.
        ---
        responses:
          200:
            description: The task was succesfully initiated
          500:
            description: Something went wrong

        tags: [Cohort]
        """
        try:
            result = query_standard_features.delay()
        except Exception as e:
            log.exception(e)
            return {
                "error": "Something went wrong when creating the task",
                "e": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"id": result.id}, HTTPStatus.OK


class QueryStandardFeature(OHDSIResource):

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
        log.debug(f"Getting status of task {id_}")
        try:
            result: AsyncResult = AsyncResult(id_)
        except Exception as e:
            log.exception(e)
            return {"error": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR

        log.debug(f"Task {id_} is in state {result.state}")
        if result.ready():
            if isinstance(result.result, pd.DataFrame):
                res: pd.DataFrame = result.result
                res = res.to_json(orient="split")
                log.info(f"Panda Dataframe converted to JSON")
            else:
                log.warning(f"Result is not a panda dataframe")
                res = str(result.result)
        else:
            res = None

        return {
            "id": id_,
            "state": result.state,
            "info": str(result.info),
            "result": res,
        }
