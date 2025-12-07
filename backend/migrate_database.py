"""
Database migration script to add user_id column to projects table
and create tokens table if it doesn't exist.
"""
import sqlite3
import os
from pathlib import Path

# Database path
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
db_path = DATABASE_URL.replace("sqlite:///", "")

if db_path == ":memory:":
    print("Cannot migrate in-memory database")
    exit(1)

# Ensure data directory exists
db_dir = Path(db_path).parent
db_dir.mkdir(parents=True, exist_ok=True)

if not os.path.exists(db_path):
    print(f"Database file {db_path} does not exist. It will be created on next app start.")
    exit(0)

print(f"Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if user_id column exists in projects table
    cursor.execute("PRAGMA table_info(projects)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'user_id' not in columns:
        print("Adding user_id column to projects table...")
        # First, set a default user_id for existing projects (use first user or NULL)
        # We'll set it to NULL and let the app handle it, or assign to first user
        cursor.execute("SELECT id FROM users LIMIT 1")
        first_user = cursor.fetchone()
        default_user_id = first_user[0] if first_user else None
        
        if default_user_id:
            # Add column with default value
            cursor.execute(f"ALTER TABLE projects ADD COLUMN user_id INTEGER REFERENCES users(id)")
            # Update existing projects to have the first user's ID
            cursor.execute(f"UPDATE projects SET user_id = {default_user_id} WHERE user_id IS NULL")
            print(f"Added user_id column and assigned existing projects to user_id {default_user_id}")
        else:
            # No users exist, just add the column as nullable
            cursor.execute("ALTER TABLE projects ADD COLUMN user_id INTEGER REFERENCES users(id)")
            print("Added user_id column (no users exist yet)")
    else:
        print("user_id column already exists in projects table")
    
    # Check if tokens table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tokens'")
    if not cursor.fetchone():
        print("Creating tokens table...")
        cursor.execute("""
            CREATE TABLE tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token VARCHAR NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        cursor.execute("CREATE INDEX ix_tokens_token ON tokens(token)")
        print("Created tokens table")
    else:
        print("tokens table already exists")
    
    conn.commit()
    print("Migration completed successfully!")
    
except sqlite3.Error as e:
    conn.rollback()
    print(f"Migration failed: {e}")
    raise
finally:
    conn.close()

