import os
import logging

from flask import Flask
from flask_restful import Api
from celery import Celery
from flasgger import Swagger

# from .old import FeatureExtraction, FeatureExtractionJob

from .resource.version import Version
from .resource.health import Health
from .resource.status import Status
from .resource.test import CountTest, ErrorTest, CeleryTest, CeleryStatus

logging.basicConfig(level=logging.DEBUG)

broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@127.0.0.1:5672")
backend_url = os.environ.get("CELERY_RESULT_BACKEND", "db+sqlite:///results.sqlite")

app = Flask(__name__)

app.config["CELERY"] = dict(
    broker=broker_url,
    result_backend=backend_url,
    task_ignore_result=True,
)

app.config["SWAGGER"] = dict(
    title="OHDSI API",
    description="API for the OHDSI project",
    version="0.1.0",
    openapi="3.0.2",
    uiversion=3,
)

swagger = Swagger(app)


api = Api(app)
celery_app = Celery(app.name)
celery_app.config_from_object(app.config["CELERY"])
celery_app.set_default()


api.add_resource(
    Version,
    "/version",
    resource_class_kwargs={
        "api": api,
        "celery": celery_app,
    },
)


api.add_resource(
    Health,
    "/health",
    resource_class_kwargs={
        "api": api,
        "celery": celery_app,
    },
)

api.add_resource(
    Status,
    "/status",
    resource_class_kwargs={
        "api": api,
        "celery": celery_app,
    },
)

api.add_resource(
    CountTest,
    "/count",
    resource_class_kwargs={
        "api": api,
        "celery": celery_app,
    },
)

api.add_resource(
    ErrorTest,
    "/error",
    resource_class_kwargs={
        "api": api,
        "celery": celery_app,
    },
)


api.add_resource(
    CeleryStatus,
    "/result/<string:id_>",
    resource_class_kwargs={
        "api": api,
        "celery": celery_app,
    },
)

api.add_resource(
    CeleryTest,
    "/celery",
    resource_class_kwargs={
        "api": api,
        "celery": celery_app,
    },
)

# api.add_resource(FeatureExtraction, "/feature-extraction")
# api.add_resource(FeatureExtractionJob, "/feature-extraction/<string:job_id>")


# celery_app.Task = FlaskTask
