from fastapi import FastAPI

from src.apis.email import router as email_router
from src.apis.sms import router as sms_router
from src.auth.controller import router as auth_router
from src.todos.controller import router as todos_router
from src.users.controller import router as users_router


def register_routes(app: FastAPI):
    app.include_router(auth_router)  # Auth routes
    app.include_router(users_router)  # User routes
    app.include_router(email_router)  # Email routes
    app.include_router(sms_router) # SMS routes
    app.include_router(todos_router) # Ejemplo routes - Example de rutas protegidas
