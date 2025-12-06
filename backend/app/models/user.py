from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()

