from http import HTTPStatus

from . import ServiceResource


class Version(ServiceResource):
    def get(self):
        """
        Reports the version of the API.

        ---
        responses:
          200:
            description: version of the server

        tags: [Monitor]
        """

        with open("/app/VERSION", "r") as f:
            version = f.read().strip()

        return {"version": version}, HTTPStatus.OK
