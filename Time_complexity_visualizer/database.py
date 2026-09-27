"""
SQLAlchemy setup for persisting analysis results.

Uses SQLite by default (a single file, zero configuration — good fit
for a small local tool like this). Everything else in the app talks
to the database only through SQLAlchemy's ORM (see models.py) — no
raw SQL strings anywhere.

To point this at a different database (Postgres, MySQL, etc.) later,
just change DATABASE_URL to the appropriate SQLAlchemy connection
string; nothing else in the app needs to change.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'analysis.db')}"

# check_same_thread=False is needed for SQLite when the same
# connection may be touched by different threads, which Flask's dev
# server can do.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db():
    """Create all tables that don't already exist. Safe to call every
    time the app starts."""
    import models  # noqa: F401  (ensures AnalysisResult is registered on Base before create_all)
    Base.metadata.create_all(bind=engine)
