from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, db: Session):
        self.project_repository = ProjectRepository(db)

    def get_all_projects_by_user(self, user_id: int) -> List[Project]:
        return self.project_repository.find_all_by_user(user_id)

    def create_project(self, project: Project) -> Project:
        return self.project_repository.save(project)

    def get_project_by_id(self, project_id: int, user_id: int) -> Optional[Project]:
        return self.project_repository.find_by_id_and_user(project_id, user_id)

    def update_project(self, project: Project) -> Project:
        return self.project_repository.save(project)

    def delete_project(self, project: Project) -> None:
        return self.project_repository.delete(project)

