import socket
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.logging import logger

db_url = settings.DATABASE_URL

# Normalize postgres:// to postgresql+psycopg:// for SQLAlchemy 2.0 / Psycopg 3 compatibility
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+psycopg://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

def is_local_postgres_active(url: str, timeout: float = 0.5) -> bool:
    """Fast non-blocking probe only for localhost PostgreSQL connections."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 5432
        if host in ("localhost", "127.0.0.1"):
            with socket.create_connection((host, port), timeout=timeout):
                return True
            return False
        return True # For remote databases, let create_engine attempt standard connection
    except Exception:
        return False

# Fast local fallback to SQLite if local PostgreSQL is inactive
if ("localhost" in db_url or "127.0.0.1" in db_url) and not is_local_postgres_active(db_url):
    logger.info("Local PostgreSQL 5432 not active, using instant SQLite fallback database.")
    db_url = "sqlite:///./chainsentinel.db"

try:
    if "postgresql" in db_url:
        engine = create_engine(
            db_url,
            connect_args={"connect_timeout": 5},
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
