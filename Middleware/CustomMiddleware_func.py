# CustomMiddleware на основе функций
# При создании промежуточного программного обеспечения на основе функций мы можем использовать декоратор
# @app.middleware("http"), поверх функции, чтобы указать,
# что функция будет действовать как промежуточное программное обеспечение.
# Это говорит FastAPI зарегистрировать функцию как компонент Middleware.

from fastapi import FastAPI, Request
import time

app = FastAPI()


@app.middleware("http")
async def modify_request_response_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"Request duration: {duration:.10f} seconds")
    return response

# request: Содержит всю информацию и данные, связанные с входящим запросом.
# call_next: Вызывая функцию call_next, промежуточное программное обеспечение гарантирует, что запрос переходит к соответствующей операции пути и ждет результирующего ответа.

@app.get("/hello")
async def greeter():
    return {"Hello": "World"}


@app.get("/goodbye")
async def farewell():
    return {"Goodbye": "World"}

