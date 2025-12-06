from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    advice_prompt = Column(Text)  # Prompt/instructions for how to describe the idea
    file_generation_prompt = Column(Text)  # Prompt for generating competition files
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name: str = None, description: str = None, advice_prompt: str = None, file_generation_prompt: str = None):
        self.name = name
        self.description = description
        self.advice_prompt = advice_prompt
        self.file_generation_prompt = file_generation_prompt
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()

