from celery import Celery

celery_app = Celery("backend", broker="redis://redis:6379/0")

@celery_app.task
def example_task():
    return "Hello from Celery!"
