import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey,
                        ForeignKeyConstraint, String)
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from src.database.types import UniversalUUID

from ..database.core import Base


class Priority(enum.Enum):
    Normal = 0
    Low = 1
    Medium = 2
    High = 3
    Top = 4


class Todo(Base):
    __tablename__ = 'todos'

    # Mantener id como String ya que así está en la base de datos
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # Mantener user_id como UniversalUUID ya que así está en la base de datos
    user_id = Column(UniversalUUID, nullable=False)
    description = Column(String(500), nullable=False)
    due_date = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False,
                        default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    priority = Column(Enum(Priority), nullable=False, default=Priority.Medium)

    # Definición de la clave foránea
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    def __repr__(self):
        return f"<Todo(description='{self.description}', due_date='{self.due_date}', is_completed={self.is_completed})>"

