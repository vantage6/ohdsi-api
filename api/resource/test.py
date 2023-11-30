# TODO read the schema from the environment variable
# TODO Test connection with a query in celery
# TODO Test connection with a query that fails
from http import HTTPStatus
from logging import getLogger
from celery.result import AsyncResult

from ohdsi.database_connector import query_sql
from ohdsi.common import RS4Extended, convert_from_r

from . import OHDSIResource
from ..task.count import count

log = getLogger(__name__)


class CountTest(OHDSIResource):
    def get(self):
        """
        Count the number of records in the person table.

        This endpoint counts the number of records in the person table. It used a
        direct SQL query to the database (So not using the celery workers).
        ---
        responses:
          200:
            description: The number of patients in the database
          500:
            description: Something went wrong

        tags: [Test]
        """
        connection = self.connect()
        log.info("Going to count the number of persons in the database")
        try:
            count = query_sql(
                connection, "SELECT COUNT(*) FROM omopcdm_synthetic.person"
            )
        except Exception as e:
            log.exception(e)
            # read /app/errorReportSql.txt and return it
            with open("/app/errorReportSql.txt", "r") as f:
                error_report = f.read()

            return {"error": str(error_report)}, HTTPStatus.INTERNAL_SERVER_ERROR

        log.info("Counted the number of persons in the database")

        count = RS4Extended.from_RS4(count)
        count = convert_from_r(count.extract("COUNT"))
        log.info("Converted from R object")

        return {"count": count}, HTTPStatus.OK


class ErrorTest(OHDSIResource):
    def get(self):
        """
        Produce an error on the query.

        This endpoint is used to test the error handling of the API.
        ---
        responses:
            500:
                description: As expected the query failed
            200:
                description: If you get this the test failed.. by succeeding

        tags: [Test]
        """

        connection = self.connect()
        log.info("Going to send a broken query to the database")
        try:
            query_sql(connection, "SELECT COUNT(*) FROM non_existing_table")
        except Exception as e:
            log.exception(e)
            # read /app/errorReportSql.txt and return it
            with open("/app/errorReportSql.txt", "r") as f:
                error_report = f.read()

            return {"error": str(error_report)}, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"msg": "If you get this the test failed.. by succeeding"}, HTTPStatus.OK


# TODO make regular resource
class CeleryTest(OHDSIResource):
    def get(self):
        """
        Create a count task.

        This endpoint creates a count task and returns the task id. This endpoint
        uses the celery workers. The result can be retrieved with the CeleryStatus
        endpoint.
        ---
        responses:
            200:
                description: Task started
            503:
                description: Celery is not available, check the health endpoint

        tags: [Test]
        """
        try:
            task: AsyncResult = count.delay()
        except Exception as e:
            log.exception(e)
            return {"error": "Celery is not available"}, HTTPStatus.SERVICE_UNAVAILABLE

        return {"id": task.id}


# TODO make regular resource
class CeleryStatus(OHDSIResource):
    def get(self, id_):
        """
        Retrieve the status and/or result of a task.

        This endpoint retrieves the status and/or result of a task. The task id is
        returned by the CeleryTest endpoint.
        ---
        responses:
            200:
                description: The number of patients in the database
            500:
                description: Something went wrong

        tags: [Test]
        """
        result = AsyncResult(id_)

        if result.ready():
            res = result.result
        else:
            res = None

        if not isinstance(res, str | dict):
            res = str(res)
            print("not a sting")
            print(res)
        else:
            print("is a string")

        return {
            "id": id_,
            "state": result.state,
            "value": res,
            "info": str(result.info),
        }, HTTPStatus.OK
