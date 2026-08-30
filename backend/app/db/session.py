import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.logging import logger

db_url = settings.DATABASE_URL

def is_postgres_connectable(host: str = "localhost", port: int = 5432, timeout: float = 0.5) -> bool:
    """Fast non-blocking socket probe to verify if PostgreSQL port is active."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

# Fast fallback to SQLite if PostgreSQL port 5432 is not connectable
if db_url.startswith("postgresql") and not is_postgres_connectable():
    logger.info("Local PostgreSQL 5432 not active, using instant SQLite fallback database.")
    db_url = "sqlite:///./chainsentinel.db"

try:
    if db_url.startswith("postgresql"):
        engine = create_engine(
            db_url,
            connect_args={"connect_timeout": 2},
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
    else:
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
except Exception as e:
    logger.warning(f"Could not connect using {db_url}, falling back to SQLite local database: {e}")
    db_url = "sqlite:///./chainsentinel.db"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
