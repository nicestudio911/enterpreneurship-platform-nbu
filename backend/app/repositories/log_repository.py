from sqlalchemy.orm import Session
from typing import List
from app.models.generation_log import GenerationLog


class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_project_id(self, project_id: int) -> List[GenerationLog]:
        return self.db.query(GenerationLog).filter(
            GenerationLog.project_id == project_id
        ).order_by(GenerationLog.created_at.asc()).all()

    def save(self, log: GenerationLog) -> GenerationLog:
        try:
            self.db.add(log)
            self.db.commit()
            self.db.refresh(log)
            return log
        except Exception:
            self.db.rollback()
            raise

    def clear_project_logs(self, project_id: int) -> None:
        """Clear all logs for a project (useful when starting new generation)"""
        try:
            self.db.query(GenerationLog).filter(
                GenerationLog.project_id == project_id
            ).delete()
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

