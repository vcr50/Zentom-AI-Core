from collections.abc import Generator
import logging
import time

from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from .config import settings
from .models import Base

DATABASE_URL = settings.database_url or "sqlite:///./zentom_api.db"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
pool_kwargs = {"poolclass": StaticPool} if DATABASE_URL == "sqlite:///:memory:" else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, **pool_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger = logging.getLogger(__name__)


def init_database(max_attempts: int = 10, retry_delay_seconds: float = 2.0) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            if DATABASE_URL.startswith("postgresql"):
                with engine.begin() as conn:
                    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if attempt == max_attempts:
                raise
            logger.warning(
                "Database unavailable during startup; retrying in %.1fs (%d/%d).",
                retry_delay_seconds,
                attempt,
                max_attempts,
            )
            time.sleep(retry_delay_seconds)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
