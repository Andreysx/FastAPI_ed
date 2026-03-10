import time

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def call_background_task(message):
    time.sleep(10)
    print(f"Background Task called!")
    print(message)


@app.get("/")
async def hello_world(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(call_background_task, message)
    return {'message': 'Hello World!'}

# BackgroundTasks не создаёт новый поток, не поднимает отдельный event loop и не организует очередь задач.
# Это просто механизм, который собирает список функций и вызывает их после отправки ответа клиенту,
# причём делает это в том же контексте выполнения, что и обработчик запроса,
# то есть в том же event loop (если функция async) или в том же потоке (если функция sync).
# Он не даёт параллелизма в смысле многопоточности или многопроцессности,
# фоновая задача не работает одновременно с обработкой других запросов, а просто выполняется после завершения эндпоинта.
