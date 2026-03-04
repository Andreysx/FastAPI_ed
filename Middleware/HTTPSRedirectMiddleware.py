from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def main():
    return {"message": "Hello World"}

# HTTPSRedirectMiddleware обеспечивает безопасность, перенаправляя все HTTP-запросы на HTTPS.
# Это важно для защиты данных пользователей, особенно при передаче конфиденциальной информации.