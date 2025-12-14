import uvicorn
from fastapi import FastAPI, Depends, Query
 # В FastAPI зависимость может быть определена либо как функция, либо как вызываемый класс.
# зависимость - это способ обернуть некоторую логику, которая извлекает некоторые подзначения или подобъекты, делает что-то с ними и,
# наконец, возвращает значение, которое будет введено в эндпоинт, вызывающую его.
app = FastAPI()



#зависимость как обычная функция
async def pagination_func(limit: int = Query(10, ge=0), page: int = 1):
    return [{'limit': limit, 'page': page}]


@app.get("/messages")
async def all_messages(pagination: list = Depends(pagination_func)):
    return {"messages": pagination}


@app.get("/comments")
async def all_comments(pagination: list = Depends(pagination_func)):
    return {"comments": pagination}


#зависимости на основе классов
# Как видите, мы создаем класс Paginator. Он содержит метод __init__.
# FastAPI анализирует параметры класса Paginator и обрабатывает их так же,
# как и параметры запроса
class Paginator:
    def __init__(self, limit: int = 10, page: int = 1):
        self.limit = limit
        self.page = page


@app.get("/users")
async def all_users(pagination: Paginator = Depends(Paginator)):
    return {"user": pagination}


#
# Зависимости на основе параметра запроса (если функция что-то возвращает и мы используем возвращаемое ей значение в нашем эндпоинте)
# Зависимости пути(Функция ничего не возвращает, а лишь принимает параметр пути и осуществляет логику фильтрации, валидации и тд)


# Глобальные зависимости
# app = FastAPI(dependencies=name_of_dependency)



if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)