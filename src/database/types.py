import uuid
from sqlalchemy.types import TypeDecorator, BINARY, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class UniversalUUID(TypeDecorator):
    """
    Tipo de columna agnóstico al motor para manejar UUIDs.
    Almacena UUIDs como:
    - nativo (UUID) en PostgreSQL,
    - BINARY(16) en otros motores como MySQL,
    - CHAR(36) en SQLite.
    """
    impl = BINARY(16)

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        elif dialect.name == 'sqlite':
            return dialect.type_descriptor(CHAR(36))
        else:  # MySQL u otros
            return dialect.type_descriptor(BINARY(16))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            if dialect.name == 'postgresql':
                return str(value)
            elif dialect.name == 'sqlite':
                return str(value)
            else:
                return value.bytes  # Convertir a bytes para MySQL
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, bytes):
            return uuid.UUID(bytes=value)
        else:
            return uuid.UUID(value)
