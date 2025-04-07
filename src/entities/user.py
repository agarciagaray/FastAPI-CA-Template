import uuid

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from src.database.types import UniversalUUID

from ..database.core import Base


class User(Base):
    __tablename__ = 'users'

    # id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # Almacena UUID como string
    # id = Column(String(36), primary_key=True)
    id = Column(UniversalUUID, primary_key=True, default=uuid.uuid4, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password_hash = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>"
