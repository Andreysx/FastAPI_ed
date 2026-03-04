from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

# TrustedHostMiddleware используется для защиты приложения от атак, связанных с подделкой заголовка Host (HTTP Host Header Attacks).
# Этот middleware проверяет, соответствует ли заголовок Host входящего запроса одному из разрешённых доменных имён.