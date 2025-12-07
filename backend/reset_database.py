"""
Script to reset/flush the database - deletes all data and recreates tables
"""
import os
from pathlib import Path
from app.database import engine, Base, init_db

# Database URL from environment variable or default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./data/app.db"
)

# Get database path
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    if db_path != ":memory:":
        db_file = Path(db_path)
        if db_file.exists():
            print(f"Deleting database file: {db_path}")
            db_file.unlink()
            print("Database file deleted")
        else:
            print(f"Database file does not exist: {db_path}")
    else:
        print("Cannot reset in-memory database")
        exit(1)
else:
    print("This script only works with SQLite databases")
    exit(1)

# Recreate all tables
print("Recreating database tables...")
init_db()
print("Database reset completed successfully!")
print("All tables have been recreated. You may need to:")
print("1. Run seed_competitions.py to populate competition data")
print("2. Create new user accounts")

