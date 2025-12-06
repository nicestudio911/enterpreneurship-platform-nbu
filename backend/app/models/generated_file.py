from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.database import Base


class GeneratedFile(Base):
    __tablename__ = "generated_files"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Store file content
    file_type = Column(String)  # e.g., 'pdf', 'docx', 'txt', 'json'
    status = Column(String, default="pending")  # pending, generating, completed, failed
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, project_id: int = None, filename: str = None, content: str = None, file_type: str = None, status: str = "pending"):
        self.project_id = project_id
        self.filename = filename
        self.content = content
        self.file_type = file_type
        self.status = status
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()

