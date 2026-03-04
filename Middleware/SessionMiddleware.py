# Сессия сайта — это механизм, который позволяет сайту помнить о пользователях и сохранять сделанные ими действия.
#
# Сессии используются для разных целей, например:
# для сохранения введённых пользователем данных;
# для настройки выдачи под интересы пользователя;
# для показа персональных предложений в зависимости от действий на сайте.
#
# Сессии делятся на два вида:
# Временные. Существуют до тех пор, пока пользователь не закроет браузер.
# Постоянные. Хранятся на компьютере в виде файлов cookie и могут быть использованы даже после выключения устройства.
# Чтобы управлять данными сеанса, нам нужно создать отдельный сеанс с помощью SessionMiddleware от Starlette.


from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="7UzGQS7woBazLUtVQJG39ywOP7J7lkPkB0UmDhMgBR8=")

# pip install itsdangerous
# Чтобы добавить данные сеанса в наш код, нам нужно внедрить
# Request в каждую службу эндпоинта и использовать ее словарь сеанса для хранения объектов области сеанса.
@app.get("/create_session")
async def session_set(request: Request):
    request.session["my_session"] = "1234"
    return 'ok'

# С другой стороны, функция session_info() получает данные сеанса my_session через request.session[] и возвращает их в качестве ответа
@app.get("/read_session")
async def session_info(request: Request):
    my_var = request.session.get("my_session")
    return my_var

# отправим GET запрос в этот эндпоинт, то данный файл Cookies будет удален.
# Мы его можем использовать когда пользователь выходит из приложения, чтобы удалить все созданные сеансы.
@app.get("/delete_session")
async def session_delete(request: Request):
    my_var = request.session.pop("my_session")
    return my_var