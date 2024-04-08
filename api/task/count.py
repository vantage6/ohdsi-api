import logging
from celery import shared_task

from ohdsi.database_connector import query_sql
from ohdsi.common import RS4Extended, convert_from_r

from . import OHDSITask

log = logging.getLogger(__name__)


@shared_task(bind=True, ignore_result=False, time_limit=60, base=OHDSITask)
def count(self):

    log.debug("Going to count the number of persons in the database")
    if not self.request.schema:
        return {"error": "No schema is set"}

    count = query_sql(
        self.request.connection, f"SELECT COUNT(*) FROM {self.request.schema}.person"
    )
    log.debug("Counted the number of persons in the database")

    count = RS4Extended.from_RS4(count)
    count = convert_from_r(count.extract("COUNT"))
    log.debug("Converted from R object")

    return count
