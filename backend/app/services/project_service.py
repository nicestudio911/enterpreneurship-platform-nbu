from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, db: Session):
        self.project_repository = ProjectRepository(db)

    def get_all_projects(self) -> List[Project]:
        return self.project_repository.find_all()

    def create_project(self, project: Project) -> Project:
        return self.project_repository.save(project)

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.project_repository.find_by_id(project_id)

    def update_project(self, project: Project) -> Project:
        return self.project_repository.save(project)

    def delete_project(self, project: Project) -> None:
        return self.project_repository.delete(project)

