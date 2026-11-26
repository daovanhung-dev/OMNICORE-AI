from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Metadata root for approved application models and Alembic migrations."""
