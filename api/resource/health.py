from http import HTTPStatus
from logging import getLogger

from . import OHDSIResource
from ..task.pong import ping

log = getLogger(__name__)


class Health(OHDSIResource):
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

        # Check OHDSI database connection
        database_status = "ok"
        try:
            self.connect()
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

        # Check Celery Backend
        celery_backend_status = "ok"
        try:
            ping_result = ping.delay()
            ping_result.get(timeout=3)
        except Exception as e:
            log.error(e)
            celery_backend_status = "Celery backend is not available"

        all_online = all([database_status == "ok", celery_status == "ok"])
        status_code = HTTPStatus.OK if all_online else HTTPStatus.SERVICE_UNAVAILABLE

        return {
            "API": "ok",
            "database": database_status,
            "celery": celery_status,
            "celery_backend": celery_backend_status,
        }, status_code
