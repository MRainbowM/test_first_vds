from celery import Celery

from .calc import calc_service
from .config import settings

celery_app = Celery(__name__)
celery_app.conf.broker_url = settings.CELERY_BROKER_URL
celery_app.conf.result_backend = settings.CELERY_RESULT_BACKEND


@celery_app.task()
def create_task(task_id: str):
    calc_service.summa(task_id=task_id)

    return True
