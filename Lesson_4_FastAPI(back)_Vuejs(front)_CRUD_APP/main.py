# Импортируем необходимые библиотеки
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# FastAPI: Основной класс для создания API, с которым мы работали в прошлых лекциях.
# CORSMiddleware: Позволяет настроить CORS для взаимодействия фронтенда Vue.js с бэкендом.
# BaseModel из pydantic: BaseModel нужен для создания моделей валидации.

# Создаём приложение FastAPI
app = FastAPI(title="Messages CRUD")
# Мы создаём экземпляр FastAPI и присваиваем его переменной app.
# Это основа нашего бэкенда, где мы будем определять эндпоинты.
# Экземпляр app — это точка входа для маршрутов и middleware.


# Настраиваем CORS для взаимодействия с фронтендом
# CORS позволяет фронтенду с одного домена (например, http://localhost:3000)
# отправлять запросы к бэкенду на другом домене (например, http://localhost:8000).
# CORS (Cross-Origin Resource Sharing) управляет кросс-доменными запросами.
# Поскольку фронтенд Vue.js будет на другом порту, чем бэкенд, нам нужен CORS.
# Vue.js: легкий и интуитивный frontend-фреймворк, подходящий для небольших и средних проектов.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Модель Pydantic для создания нового сообщения(POST, PUT)
class MessageCreate(BaseModel):
    content: str


# Модель Pydantic для частичного обновления сообщения
# content это опциональное поле, можно не указывать или передать None. Подходит для PATCH-запросов.
class MessageUpdate(BaseModel):
    content: str | None = None


# Модель Pydantic для представления сообщения в ответах API(GET)
# Определяет структуру ответа API
# Эта модель будет использоваться в GET-эндпоинтах для возврата сообщений в Vue.js
class Message(BaseModel):
    id: int
    content: str


# Простая "база данных" в памяти для хранения сообщений
messages_db: list[Message] = [Message(id=0, content="First post in FastAPI")]


# Функция для генерации следующего уникального ID для нового сообщения
def next_id() -> int:
    return max((m.id for m in messages_db), default=-1) + 1


# Эндпоинт для получения списка сообщений
# Он позволяет фронтенду получить все сообщения для отображения в интерфейсе.
@app.get("/messages", response_model=list[Message])
async def list_messages() -> list[Message]:
    return messages_db


# Эндпоинт для создания сообщения
# Он позволяет фронтенду отправлять новые сообщения, которые сохраняются в messages_db.
@app.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(payload: MessageCreate) -> Message:
    m = Message(id=next_id(), content=payload.content)
    messages_db.append(m)
    return m



# Вспомогательная функция для получения индекса сообщения по ID
# Она упрощает поиск сообщений по ID в операциях обновления и замены, избегая дублирования кода.
# Вспомогательные функции делают код более читаемым и переиспользуемым.
# Мы будем использовать get_index в эндпоинтах PUT и PATCH.
def get_index(message_id: int) -> int:
    for i, m in enumerate(messages_db):
        if m.id == message_id:
            return i
    return -1



# Эндпоинт для получения одного сообщения
@app.get("/messages/{message_id}", response_model=Message)
async def get_message(message_id: int) -> Message:
    idx = get_index(message_id)
    if idx < 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return messages_db[idx]


# Эндпоинт для частичного обновления сообщения
# Теперь добавим эндпоинт для частичного обновления сообщения.
# PATCH позволяет обновлять только определённые поля,
# что экономит трафик и делает API более гибким.
@app.patch("/messages/{message_id}", response_model=Message)
async def update_message(message_id: int, payload: MessageUpdate) -> Message:
    # Ищем индекс сообщения по ID
    idx = get_index(message_id)

    # Если сообщение не найдено, возвращаем ошибку 404
    if idx < 0:
        raise HTTPException(status_code=404, detail="Message not found")

    # Обновляем только переданные поля
    if payload.content is not None:
        messages_db[idx].content = payload.content

    return messages_db[idx]


# Эндпоинт для полной замены сообщения
# Добавим еще PUT-эндпоинт для полной замены сообщения.
# PUT требует полного набора данных и полностью заменяет ресурс,
# тогда как PATCH обновляет только указанные поля.
# Главная разница с PATCH, в том, что PUT требует полного набора данных и полностью заменяет ресурс,
# тогда как PATCH обновляет только указанные поля.
# PUT всегда используется для полной замены ресурса.
# Если передать неполные данные, Pydantic вернёт ошибку валидации.
# Это отличается от PATCH, где поля могут быть опциональными.
@app.put("/messages/{message_id}", response_model=Message)
async def replace_message(message_id: int, payload: MessageCreate) -> Message:
    idx = get_index(message_id)
    if idx < 0:
        raise HTTPException(status_code=404, detail="Message not found")
    updated = Message(id=message_id, content=payload.content)
    messages_db[idx] = updated
    return updated


# Эндпоинт для удаления сообщения
# В этом случае DELETE возвращает только статус 204, без тела ответа.
@app.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: int):
    # Ищем индекс сообщения по ID
    idx = get_index(message_id)

    # Если сообщение не найдено, возвращаем ошибку 404
    if idx < 0:
        raise HTTPException(status_code=404, detail="Message not found")

    # Удаляем сообщение из базы данных
    messages_db.pop(idx)