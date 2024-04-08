from http import HTTPStatus

from . import ServiceResource


class Status(ServiceResource):
    def get(self):
        """
        Check the status of the Celery workers.

        This endpoint checks the status of the Celery workers.
        ---
        responses:
          200:
            description: Detailed status of the Celery workers

        tags: [Monitor]
        """

        control = self.celery.control.inspect()
        availability = self.celery.control.ping(timeout=1)
        stats = control.stats()
        registered_tasks = control.registered()
        active_tasks = control.active()
        scheduled_tasks = control.scheduled()

        return {
            "availability": availability,
            "stats": stats,
            "registered_tasks": registered_tasks,
            "active_tasks": active_tasks,
            "scheduled_tasks": scheduled_tasks,
        }, HTTPStatus.OK
