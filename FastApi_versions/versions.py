# 1. Версионирование на основе пути с использованием префикса URL:
# Лучшее решение - использовать подприложения для разделения каждой версии вашего API на собственный объект приложения.
from fastapi import FastAPI, APIRouter, HTTPException

# Основное приложение
app = FastAPI(
    title="My API",
    description="API with versioned endpoints",
    version="1.0.0"
)

# Роутер для версии 1
router_v1 = APIRouter(prefix="/v1", tags=["v1"])


@router_v1.get("/products")
async def get_products_v1():
    return {"message": "Products API Version 1"}


# Роутер для версии 2
router_v2 = APIRouter(prefix="/v2", tags=["v2"])


@router_v2.get("/products")
async def get_products_v2():
    return {"message": "Products API Version 2"}


# Подключение роутеров к основному приложению
app.include_router(router_v1)
app.include_router(router_v2)

# 2. Управление версиями URL:
#
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/v1/products")
# async def get_products_v1():
#     return {"message": "Products API Version 1"}
#
#
# @app.get("/v2/products")
# async def get_products_v2():
#     return {"message": "Products API Version 2"}
#
# 3. Управление версиями параметров запроса:
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/products/")
# async def get_products(version: int = 1):
#     if version == 1:
#         return {"message": "Products API Version 1"}
#     elif version == 2:
#         return {"message": "Products API Version 2"}



