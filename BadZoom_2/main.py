from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, validator
from typing import List
import hashlib

app = FastAPI(title="Система регистрации", version="1.0.0")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем шаблоны
templates = Jinja2Templates(directory="templates")


# Модель для валидации данных
class UserRegistration(BaseModel):
    email: str
    first_name: str
    last_name: str
    middle_name: str
    password: str
    password_confirm: str
    position: str

    @validator('first_name', 'last_name', 'middle_name')
    def name_must_not_be_empty(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Имя не может быть пустым')
        return v.strip()

    @validator('password_confirm')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v

    @validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль должен содержать минимум 6 символов')
        return v


# Хранилище пользователей (в реальном проекте используй базу данных!)
users_db: List[dict] = []


def hash_password(password: str) -> str:
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()


# Главная страница - форма регистрации
@app.get("/", response_class=HTMLResponse)
async def registration_form(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "title": "Регистрация пользователя"
        }
    )


# Обработка формы регистрации
@app.post("/register")
async def register_user(
        request: Request,
        email: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        middle_name: str = Form(...),
        password: str = Form(...),
        password_confirm: str = Form(...),
        position: str = Form(...)
):
    try:
        # Валидация данных с помощью Pydantic
        user_data = UserRegistration(
            email=email,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            password=password,
            password_confirm=password_confirm,
            position=position
        )

        # Проверяем не занят ли email
        if any(user['email'] == email for user in users_db):
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

        # Сохраняем пользователя (в реальном проекте - в базу данных)
        user_record = {
            "id": len(users_db) + 1,
            "email": user_data.email,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "middle_name": user_data.middle_name,
            "position": user_data.position,
            "password_hash": hash_password(user_data.password)
            # В реальном проекте никогда не храните пароли в открытом виде!
        }
        users_db.append(user_record)

        # Перенаправляем на страницу успеха
        return templates.TemplateResponse(
            "success.html",
            {
                "request": request,
                "user": user_record,
                "title": "Регистрация успешна!"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Страница списка пользователей
@app.get("/users", response_class=HTMLResponse)
async def users_list(request: Request):
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users_db,
            "title": "Список пользователей"
        }
    )


# API для получения списка пользователей (JSON)
@app.get("/api/users")
async def get_users_api():
    return {"users": users_db, "total": len(users_db)}


# API для очистки пользователей (для тестирования)
@app.delete("/api/users/clear")
async def clear_users():
    users_db.clear()
    return {"message": "Все пользователи удалены"}


# Запуск приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)