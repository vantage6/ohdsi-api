from flask_restful import Resource


class ServiceResource(Resource):

    def __init__(self, api, celery):
        self.api = api
        self.celery = celery


class OHDSIResource(ServiceResource):

    @staticmethod
    def connect():
        pass
