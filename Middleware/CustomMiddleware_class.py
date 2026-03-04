# CustomMiddleware на основе классов
# Middleware в FastAPI обрабатывает запросы перед их отправкой в определенные операции пути, и обрабатывает ответы перед их возвратом.
# Это делает его идеальным для общих операций, которые мы хотим выполнять по каждому запросу и ответу, таких как регистрация времени между запросом и его ответом.
from fastapi import FastAPI
import time


class TimingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start_time = time.time()
        await self.app(scope, receive, send)
        duration = time.time() - start_time
        print(f"Request duration: {duration:.10f} seconds")


app = FastAPI()
app.add_middleware(TimingMiddleware)


@app.get("/hello")
async def greeter():
    return {"Hello": "World"}


@app.get("/goodbye")
async def farewell():
    return {"Goodbye": "World"}

# программное обеспечение будет работать каждый раз, когда мы запрашиваем один из маршрутов API.
# при расширении возможностей - если функция __call__ нашего Middleware содержит слишком много обработки, это замедлит все наше приложение.