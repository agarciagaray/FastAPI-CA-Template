from fastapi import FastAPI

from .api import register_routes
from .database.core import Base, engine
from .entities.todo import Todo  # Import models to register them
from .entities.user import User  # Import models to register them
from .logging import LogLevels, configure_logging

configure_logging(LogLevels.info)

app = FastAPI(
    title="Clean Architecture Template",
    description="""
Este proyecto es un template basado en Clean Architecture usando FastAPI.

**¿Qué incluye este template?**

- Capa de dominio con entidades de ejemplo.
- Capa de aplicación con abstracciones para casos de uso y preocupaciones transversales (logging, validación).
- Capa de infraestructura con:
- Autenticación
- SQLAlchemy y soporte para PostgreSQL, MySQL y SQLite.
- Pruebas unitarias y de integración con Pytest.
- Logging con soporte para diferentes niveles de log.
- Envío de correos electrónicos y SMS (Twilio).
- Rate limiting en el registro de usuarios
- Proyecto de pruebas:
- Pruebas unitarias con Pytest
- Pruebas de integración (e2e) con Pytest
""",
    version="1.0.0"
)

""" Only uncomment below to create new tables, 
otherwise the tests will fail if not connected
"""
# Base.metadata.create_all(bind=engine)

register_routes(app)
