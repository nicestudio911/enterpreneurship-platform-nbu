from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, token: str = None, user_id: int = None):
        self.token = token
        self.user_id = user_id
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()

