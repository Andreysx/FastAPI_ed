from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://example.com",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
# CORS - это полезная функция для веб-приложений, которым необходимо взаимодействовать с API, размещенными на разных серверах или доменах.
# FastAPI позволяет легко включать и настраивать CORS для ваших конечных точек API всего за несколько строк кода.
# allow_origins: Список источников (доменов), которым разрешен доступ к вашему API
# публичное апи - ставим allow_origins=[*] (для явности) или просто не указываем
# апи для фронта - ставим в allow_origins адрес/домен нашего фронта
# апи для серверов/приложух - ставим allow_origins=[] (потому что так лучше для zero trust)