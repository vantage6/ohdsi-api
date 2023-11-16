import os

from http import HTTPStatus
from logging import getLogger

from ohdsi.database_connector import create_connection_details, connect

from . import ServiceResource


dbms = os.environ["OMOP_DBMS"]
server = os.environ["OMOP_SERVER"]
database = os.environ["OMOP_DATABASE"]
user = os.environ["OMOP_USER"]
password = os.environ["OMOP_PASSWORD"]
port = os.environ["OMOP_PORT"]

log = getLogger(__name__)


class Health(ServiceResource):
    def get(self):
        """
        Check the health of the API.

        This endpoint checks the health of the following services:
        - API
        - Database
        - Celery
        ---
        responses:
          200:
            description: All services are healthy
          403:
            description: At least one service is not healthy

        tags: [Monitor]
        """

        # Check database connection
        database_status = "ok"
        try:
            connection_details = create_connection_details(
                dbms,
                server=f"{server}/{database}",
                user=user,
                password=password,
                port=port,
            )
            connect(connection_details)
        except Exception as e:
            log.error(e)
            database_status = "Database is not available"

        # Check Celery
        celery_status = "ok"
        try:
            self.celery.control.ping()
        except Exception as e:
            log.error(e)
            celery_status = "Celery is not available"

        all_online = all([database_status == "ok", celery_status == "ok"])
        status_code = HTTPStatus.OK if all_online else HTTPStatus.SERVICE_UNAVAILABLE

        return {
            "API": "ok",
            "database": database_status,
            "celery": celery_status,
        }, status_code
