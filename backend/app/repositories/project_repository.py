from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Project]:
        return self.db.query(Project).all()

    def find_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def save(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        try:
            self.db.delete(project)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

