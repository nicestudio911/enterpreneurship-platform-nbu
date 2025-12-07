from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Database URL from environment variable or default
# SQLite database will be stored in the data directory
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./data/app.db"
)

# Create data directory if it doesn't exist (for SQLite)
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    if db_path != ":memory:":
        db_dir = Path(db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

# SQLite requires check_same_thread=False for FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    from app.models.user import User
    from app.models.project import Project
    from app.models.competition import Competition
    from app.models.generated_file import GeneratedFile
    from app.models.generation_log import GenerationLog
    from app.models.token import Token
    Base.metadata.create_all(bind=engine)

