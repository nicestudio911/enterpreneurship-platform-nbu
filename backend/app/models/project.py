from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)  # Changed to Text for longer idea descriptions
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=True)
    idea_description = Column(Text)  # The detailed idea description
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name: str = None, description: str = None, competition_id: int = None, idea_description: str = None):
        self.name = name
        self.description = description
        self.competition_id = competition_id
        self.idea_description = idea_description

