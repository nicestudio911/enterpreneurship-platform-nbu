from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.database import Base


class GenerationLog(Base):
    __tablename__ = "generation_logs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    message = Column(Text, nullable=False)
    log_type = Column(String, default="info")  # info, success, error, warning
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, project_id: int = None, message: str = None, log_type: str = "info"):
        self.project_id = project_id
        self.message = message
        self.log_type = log_type
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()

