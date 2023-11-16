import os

from flask import Flask
from flask_restful import Api
from celery import Celery
from flasgger import Swagger

from .old import FeatureExtraction, FeatureExtractionJob

from .resource.health import Health
from .resource.status import Status

broker_url = os.environ["CELERY_BROKER_URL"] or "amqp://guest:guest@127.0.0.1:5672"
backend_url = os.environ["CELERY_RESULT_BACKEND"] or "db+sqlite:///results.sqlite"

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
    contact={"name": "OHDSI", "url": "https://ohdsi.org/", "email": ""},
    license={"name": "MIT", "url": ""},
)

swagger = Swagger(app)


api = Api(app)
celery_app = Celery(app.name)
celery_app.config_from_object(app.config["CELERY"])
celery_app.set_default()


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

api.add_resource(FeatureExtraction, "/feature-extraction")
api.add_resource(FeatureExtractionJob, "/feature-extraction/<string:job_id>")


# celery_app.Task = FlaskTask
