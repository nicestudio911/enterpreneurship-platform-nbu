from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.dependencies import get_current_user
from app.services.project_service import ProjectService
from app.models.project import Project
from app.models.user import User

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None  # Optional, can be empty since we use idea_description
    competition_id: int | None = None
    idea_description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    idea_description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    competition_id: int | None
    idea_description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=List[ProjectResponse])
def get_all_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project_service = ProjectService(db)
    projects = project_service.get_all_projects_by_user(current_user.id)
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project_service = ProjectService(db)
    project = project_service.get_project_by_id(project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate required fields
    if not project_data.name or not project_data.name.strip():
        raise HTTPException(status_code=400, detail="Project name is required")
    if not project_data.idea_description or not project_data.idea_description.strip():
        raise HTTPException(status_code=400, detail="Idea description is required")
    
    project_service = ProjectService(db)
    project = Project(
        name=project_data.name.strip(),
        description=project_data.description,
        competition_id=project_data.competition_id,
        idea_description=project_data.idea_description.strip(),
        user_id=current_user.id
    )
    saved_project = project_service.create_project(project)
    return saved_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project_service = ProjectService(db)
    project = project_service.get_project_by_id(project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update only provided fields
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    if project_data.idea_description is not None:
        project.idea_description = project_data.idea_description
    
    updated_project = project_service.update_project(project)
    return updated_project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project and all associated files"""
    from app.repositories.file_repository import FileRepository
    from app.repositories.log_repository import LogRepository
    
    project_service = ProjectService(db)
    project = project_service.get_project_by_id(project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Delete associated files and logs first
        file_repository = FileRepository(db)
        log_repository = LogRepository(db)
        
        file_repository.delete_by_project_id(project_id)
        log_repository.clear_project_logs(project_id)
        
        # Delete the project
        project_service.delete_project(project)
        return {"message": "Project deleted successfully", "project_id": project_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")

