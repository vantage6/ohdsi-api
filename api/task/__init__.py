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

log = logging.getLogger(__name__)


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

        self.log_stream = io.StringIO()
        self.connection = None

        signals.task_prerun.connect(self.on_task_prerun)
        # signals.task_success.connect(self.on_task_success)

    def on_task_prerun(self, task_id, task, *args, **kwargs):
        # self.update_state(state='PROGRESS', meta={'current': 2, 'total': 10})
        log.info("Creating connection details")

        self.update_state(state="INITIALIZE", meta={"step": 1, "steps": 5})
        connection_details = create_connection_details(
            self.dbms,
            server=f"{self.server}/{self.database}",
            user=self.user,
            password=self.password,
            port=self.port,
        )

        log.info("Connecting to database")
        self.update_state(state="CONNECT", meta={"step": 2, "steps": 5})
        with redirect_stdout(self.log_stream):
            self.connection = connect(connection_details)

    def on_task_success(self, result, **kwargs):
        log.info("Disconnecting from database")
        # TODO: this part is not returned to the client
        # with redirect_stdout(self.log_stream):
        disconnect(self.connection)
