from celery import Celery

from .calc import calc_service

celery_app = Celery(__name__)
celery_app.conf.broker_url = "redis://localhost:6379"
celery_app.conf.result_backend = "redis://localhost:6379"


@celery_app.task()
def create_task(task_id: str):
    calc_service.summa(task_id=task_id)

    return True
