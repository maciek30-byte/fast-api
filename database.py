import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = Path(__file__).resolve().parent
SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # type: ignore[attr-defined]


def get_db():
    """Database session dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]