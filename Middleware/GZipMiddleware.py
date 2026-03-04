from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/")
async def main():
    return "somebigcontent"

# GZipMiddleware сжимает ответы сервера с использованием алгоритма GZip, что уменьшает объём передаваемых данных и ускоряет загрузку страниц в браузере.
# minimum_size, это - минимальный размер ответа в байтах, при котором применяется сжатие. По умолчанию равен 500 байтам.
# Это помогает избежать сжатия маленьких ответов, где затраты на сжатие могут превысить выгоду.
