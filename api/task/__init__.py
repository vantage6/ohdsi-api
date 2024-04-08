import sys
import os
import io
import logging

from contextlib import redirect_stdout

from celery import Task, signals
from ohdsi.database_connector import (
    create_connection_details,
    connect,
    disconnect,
)

log_stream = io.StringIO()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.StreamHandler()],
)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class OHDSITask(Task):

    def __init__(self):
        super().__init__()

        self.dbms = os.environ.get("OMOP_DBMS")
        self.server = os.environ.get("OMOP_SERVER")
        self.database = os.environ.get("OMOP_DATABASE")
        self.user = os.environ.get("OMOP_USER")
        self.password = os.environ.get("OMOP_PASSWORD")
        self.port = os.environ.get("OMOP_PORT")
        self.schema = os.environ.get("OMOP_CDM_SCHEMA")
        self.result_schema = os.environ.get("OMOP_RESULT_SCHEMA")

        self.connection = None

        signals.task_prerun.connect(self.on_task_prerun)
        signals.task_success.connect(self.on_task_success)

    def on_task_prerun(self, task_id, task, *args, **kwargs):
        # self.update_state(state='PROGRESS', meta={'current': 2, 'total': 10})
        log.debug("Creating connection details")
        self.update_state(state="INITIALIZE")
        connection_details = create_connection_details(
            self.dbms,
            server=f"{self.server}/{self.database}",
            user=self.user,
            password=self.password,
            port=self.port,
        )

        log.debug("Connecting to database")
        task.update_state(state="CONNECTING")
        self.connection = connect(connection_details)

        task.request.update(
            {
                "schema": self.schema,
                "result_schema": self.result_schema,
                "connection": self.connection,
                "dbms": self.dbms,
            }
        )
        task.update_state(state="EXECUTING")

    def on_task_success(self, result, **kwargs):
        log.debug("Disconnecting from database")
        # TODO: return the logstream to the user
        print(log_stream.getvalue())
        disconnect(self.connection)
