from fastapi import FastAPI

app = FastAPI(title="My First Project", summary="My CRUD application.", description="The CRUD application supports **writing**, *reading*, updating, and deleting posts.",
              version="0.0.1", openapi_url="/api/v1/openapi.json", servers=[
    {"url": "https://stag.example.com", "description": "Staging"},
    {"url": "https://prod.example.com", "description": "Production"}
])

@app.get(path='/')
async def welcome() -> dict:
    return {"message": "Hello, FastApi"}

# FastAPI автоматически преобразует возвращаемый словарь в JSON-ответ, соответствующий стандарту REST.

#параметры пути
# @app.get("/hello/{user}")
# async def welcome_user(user: str) -> dict:
#     return {"user": f'Hello {user}'}

@app.get("/hello/{first_name}/{last_name}")
async def welcome_user(first_name: str, last_name: str) -> dict:
    return {"user": f"Hello {first_name} {last_name}"}

#параметр пути
@app.get("/order/{order_id}")
async def order(order_id: int) -> dict:
    return {"id": order_id}

#параметры запроса
@app.get("/user")
async def login(username: str, age: int) -> dict:
    return {"user": username, "age": age}


#комбинация, параметров пути и параметров запроса
@app.get("/employee/{name}/company/{company}")
async def get_employee(name: str, department: str, company: str) -> dict:
    return {"Employee": name, "Company": company, "Department": department}


# Чтобы сделать параметр полностью необязательным, можно использовать значение по умолчанию None:
# @app.get("/user")
# async def login(username: str, age: int | None = None) -> dict:
#     return {"user": username, "age": age}

 # uvicorn api:app --port 8080 --reload
