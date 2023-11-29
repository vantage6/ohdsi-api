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
        Count the number of persons in the database.
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
        Produce an error on the query, and return something useful to the user.
        ---
        responses:
            200:
                description: The number of patients in the database

        tags: [Test]
        """

        connection = self.connect()
        log.info("Going to send a broken query to the database")
        try:
            count = query_sql(connection, "SELECT COUNT(*) FROM non_existing_table")
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


# TODO make regular resource
class CeleryTest(OHDSIResource):
    def get(self):
        """
        Test Celery.
        ---
        responses:
            200:
                description: Task started
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
        Test Celery.
        ---
        responses:
            200:
                description: The number of patients in the database
        """
        # id_ = "b06a84c8-114b-42f1-95a0-a209eb431163"
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
        }
