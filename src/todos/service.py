import logging
import uuid
from typing import List, Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.auth.models import TokenData
from src.entities.todo import Todo
from src.exceptions import TodoCreationError, TodoNotFoundError

from . import models

def create_todo(current_user: TokenData, db: Session, todo: models.TodoCreate) -> Todo:
    try:
        new_todo = Todo(**todo.model_dump())
        new_todo.user_id = current_user.get_uuid()
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        logging.info(f"Created new todo for user: {current_user.get_uuid()}")
        return new_todo
    except Exception as e:
        logging.error(
            f"Failed to create todo for user {current_user.get_uuid()}. Error: {str(e)}")
        raise TodoCreationError(str(e))


def get_todos(current_user: TokenData, db: Session) -> list[models.TodoResponse]:
    todos = db.query(Todo).filter(
        Todo.user_id == current_user.get_uuid()).all()
    logging.info(
        f"Retrieved {len(todos)} todos for user: {current_user.get_uuid()}")
    return todos


# def get_todo_by_id(current_user: TokenData, db: Session, todo_id: UUID) -> Todo:
#     todo = db.query(Todo).filter(Todo.id == todo_id).filter(
#         Todo.user_id == current_user.get_uuid()).first()
#     if not todo:
#         logging.warning(
#             f"Todo {todo_id} not found for user {current_user.get_uuid()}")
#         raise TodoNotFoundError(todo_id)
#     logging.info(
#         f"Retrieved todo {todo_id} for user {current_user.get_uuid()}")
#     return todo

def get_todo_by_id(current_user: TokenData, db: Session, todo_id: UUID) -> Todo:
    # Convertir todo_id a string ya que así se almacena en la base de datos
    todo_id_str = str(todo_id)

    # Obtener el UUID del usuario en formato binario
    user_id_bytes = current_user.get_uuid().bytes if isinstance(
        current_user.get_uuid(), UUID) else current_user.get_uuid()

    # Añadir logs para depuración
    logging.debug(f"Buscando Todo con ID (string): {todo_id_str}")
    logging.debug(f"Para usuario con ID (bytes): {user_id_bytes}")

    # Primero verificar si el Todo existe sin filtrar por usuario
    todo_exists = db.query(Todo).filter(Todo.id == todo_id_str).first()
    if todo_exists:
        logging.debug(
            f"Todo existe, verificando si pertenece al usuario correcto")

        # Comparar user_id directamente para depuración
        if todo_exists.user_id == user_id_bytes:
            logging.debug("¡Coincidencia exacta de user_id!")
        else:
            logging.debug(
                f"No coincide: Todo.user_id={todo_exists.user_id}, user_id_bytes={user_id_bytes}")

    # Consulta principal
    todo = db.query(Todo).filter(Todo.id == todo_id_str).filter(
        Todo.user_id == user_id_bytes).first()

    if not todo:
        logging.warning(
            f"Todo {todo_id} not found for user {current_user.get_uuid()}")

        # Intento alternativo: buscar el Todo y verificar manualmente
        alt_todo = db.query(Todo).filter(Todo.id == todo_id_str).first()
        if alt_todo:
            logging.warning(
                f"Todo existe pero con user_id diferente: {alt_todo.user_id}")

        raise TodoNotFoundError(todo_id)

    logging.info(
        f"Retrieved todo {todo_id} for user {current_user.get_uuid()}")
    return todo

# Función para depurar problemas de UUID


def debug_todo_user_ids(db: Session):
    """
    Función para depurar problemas con los IDs de usuarios en los Todos
    """
    todos = db.query(Todo).limit(5).all()

    for todo in todos:
        logging.debug(f"Todo ID: {todo.id}, tipo: {type(todo.id)}")
        logging.debug(f"User ID: {todo.user_id}, tipo: {type(todo.user_id)}")

        # Intentar convertir user_id a diferentes formatos para ver cuál coincide
        if hasattr(todo.user_id, 'hex'):
            logging.debug(f"User ID (hex): {todo.user_id.hex}")

        # Si es bytes, intentar convertirlo a UUID
        if isinstance(todo.user_id, bytes):
            try:
                uuid_obj = uuid.UUID(bytes=todo.user_id)
                logging.debug(f"User ID (como UUID): {uuid_obj}")
            except Exception as e:
                logging.debug(f"Error al convertir bytes a UUID: {e}")


def update_todo(current_user: TokenData, db: Session, todo_id: UUID, todo_update: models.TodoCreate) -> Todo:
    todo_data = todo_update.model_dump(exclude_unset=True)
    db.query(Todo).filter(Todo.id == todo_id).filter(
        Todo.user_id == current_user.get_uuid()).update(todo_data)
    db.commit()
    logging.info(
        f"Successfully updated todo {todo_id} for user {current_user.get_uuid()}")
    return get_todo_by_id(current_user, db, todo_id)


def complete_todo(current_user: TokenData, db: Session, todo_id: UUID) -> Todo:
    todo = get_todo_by_id(current_user, db, todo_id)
    if todo.is_completed:
        logging.debug(f"Todo {todo_id} is already completed")
        return todo
    todo.is_completed = True
    todo.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(todo)
    logging.info(
        f"Todo {todo_id} marked as completed by user {current_user.get_uuid()}")
    return todo


def delete_todo(current_user: TokenData, db: Session, todo_id: UUID) -> None:
    todo = get_todo_by_id(current_user, db, todo_id)
    db.delete(todo)
    db.commit()
    logging.info(f"Todo {todo_id} deleted by user {current_user.get_uuid()}")
