from fastapi import FastAPI
from celery import Celery
from task import call_background_task

app = FastAPI()

celery = Celery(
    __name__,
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0',
    broker_connection_retry_on_startup=True
)


@app.get("/")
async def hello_world(message: str):
    call_background_task.apply_async(args=[message], expires=3600)
    return {'message': 'Hello World!'}


celery.conf.beat_schedule = {
    'run-me-background-task': {
        'task': 'task.call_background_task',
        'schedule': 60.0,
        'args': ('Test text message',)
    }
}
# В Celery периодические задачи (periodic tasks) — это задачи, которые выполняются автоматически
# через определённые интервалы времени
# или в запланированные моменты.
# Для их реализации в Celery используется компонент celery beat
# task.call_background_task запускается каждые 60 секунд, используя брокер Redis.
# И именно Celery Beat отправляет задачу task.call_background_task в очередь Redis каждые 60 секунд.


# from celery.schedules import crontab
#
#
# celery.conf.beat_schedule = {
#     'run-me-background-task': {
#         'task': 'task.call_background_task',
#         'schedule': crontab(hour=7, minute=0),
#         'args': ('Test text message',)
#     }
# }