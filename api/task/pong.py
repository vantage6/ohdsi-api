from celery import shared_task


@shared_task(bind=True, ignore_result=False, time_limit=60)
def ping(self):
    return "pong"
