import os
from logging import getLogger
from flask_restful import Resource

from ohdsi.database_connector import create_connection_details, connect


log = getLogger(__name__)


class ServiceResource(Resource):
    def __init__(self, api, celery):
        self.api = api
        self.celery = celery


class OHDSIResource(ServiceResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dbms = os.environ.get("OMOP_DBMS")
        self.server = os.environ.get("OMOP_SERVER")
        self.database = os.environ.get("OMOP_DATABASE")
        self.user = os.environ.get("OMOP_USER")
        self.password = os.environ.get("OMOP_PASSWORD")
        self.port = os.environ.get("OMOP_PORT")
        self.schema = os.environ.get("OMOP_CDM_SCHEMA")

        log.info(
            "Connection details:"
            f"dbms: {self.dbms}, "
            f"server: {self.server}, "
            f"database: {self.database}, "
            f"user: {self.user}, "
            f"port: {self.port}, "
            f"schema: {self.schema}"
        )

        self.connection_details = create_connection_details(
            self.dbms,
            server=f"{self.server}/{self.database}",
            user=self.user,
            password=self.password,
            port=self.port,
        )

    def connect(self):
        return connect(self.connection_details)
