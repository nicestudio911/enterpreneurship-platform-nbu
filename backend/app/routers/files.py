from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import zipfile
import io
from app.database import get_db
from app.services.file_generation_service import FileGenerationService
from app.repositories.file_repository import FileRepository
from app.repositories.log_repository import LogRepository
from app.models.generated_file import GeneratedFile
from app.models.generation_log import GenerationLog

router = APIRouter(prefix="/api/files", tags=["files"])


class FileResponse(BaseModel):
    id: int
    project_id: int
    filename: str
    file_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FileContentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    content: str

    class Config:
        from_attributes = True


class LogResponse(BaseModel):
    id: int
    project_id: int
    message: str
    log_type: str
    created_at: datetime

    class Config:
        from_attributes = True


def generate_files_task(project_id: int):
    """Background task for file generation - creates its own DB session"""
    from app.database import SessionLocal
    import traceback
    import sys
    db = SessionLocal()
    try:
        # Log that we're starting
        log_repository = LogRepository(db)
        log_repository.save(GenerationLog(project_id=project_id, message="🚀 Background task started", log_type="info"))
        db.commit()
        
        file_service = FileGenerationService(db)
        file_service.generate_files_for_project(project_id)
        db.commit()  # Ensure all changes are committed
    except Exception as e:
        # Log error to database
        try:
            log_repository = LogRepository(db)
            error_msg = f"❌ Fatal Error: {str(e)}\n{traceback.format_exc()}"
            log = GenerationLog(project_id=project_id, message=error_msg, log_type="error")
            log_repository.save(log)
            db.commit()
            
            # Also print to console for debugging
            print(f"ERROR in background file generation for project {project_id}:", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
        except Exception as log_error:
            # If we can't log to DB, at least print it
            print(f"Error in background file generation: {str(e)}", file=sys.stderr)
            print(f"Also failed to log error: {str(log_error)}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
    finally:
        db.close()


@router.post("/generate/{project_id}")
def generate_files(project_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Start file generation for a project (runs in background)"""
    # Verify project exists
    from app.models.project import Project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Run generation in background
        background_tasks.add_task(generate_files_task, project_id)
        return {"message": "File generation started", "project_id": project_id, "status": "generating"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start file generation: {str(e)}")


@router.post("/generate/{project_id}/file/{filename}")
def regenerate_single_file(project_id: int, filename: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Regenerate a specific file for a project"""
    from app.models.project import Project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Delete the specific file if it exists
        file_repository = FileRepository(db)
        existing_files = file_repository.find_by_project_id(project_id)
        for file in existing_files:
            if file.filename == filename and file.status == "completed":
                file_repository.delete(file)
                break
        
        # Run generation in background (will regenerate all files, but we'll filter in the service)
        background_tasks.add_task(generate_single_file_task, project_id, filename)
        return {"message": f"File regeneration started for {filename}", "project_id": project_id, "filename": filename, "status": "generating"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start file regeneration: {str(e)}")


def generate_single_file_task(project_id: int, filename: str):
    """Background task for single file generation"""
    from app.database import SessionLocal
    import traceback
    import sys
    db = SessionLocal()
    try:
        # Log that we're starting
        log_repository = LogRepository(db)
        log_repository.save(GenerationLog(project_id=project_id, message=f"🔄 Background task started for {filename}", log_type="info"))
        db.commit()
        
        file_service = FileGenerationService(db)
        file_service.generate_single_file_for_project(project_id, filename)
        db.commit()  # Ensure all changes are committed
    except Exception as e:
        try:
            log_repository = LogRepository(db)
            error_msg = f"❌ Fatal Error: {str(e)}\n{traceback.format_exc()}"
            log = GenerationLog(project_id=project_id, message=error_msg, log_type="error")
            log_repository.save(log)
            db.commit()
            
            # Also print to console for debugging
            print(f"ERROR in background single file generation for project {project_id}, file {filename}:", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
        except Exception as log_error:
            print(f"Error in background file generation: {str(e)}", file=sys.stderr)
            print(f"Also failed to log error: {str(log_error)}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
    finally:
        db.close()


@router.get("/project/{project_id}", response_model=List[FileResponse])
def get_project_files(project_id: int, db: Session = Depends(get_db)):
    """Get all files for a project"""
    file_repository = FileRepository(db)
    files = file_repository.find_by_project_id(project_id)
    return files


@router.get("/{file_id}/content", response_model=FileContentResponse)
def get_file_content(file_id: int, db: Session = Depends(get_db)):
    """Get file content for preview"""
    file_repository = FileRepository(db)
    file = file_repository.find_by_id(file_id)
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file.status != "completed":
        raise HTTPException(status_code=400, detail="File is not ready for viewing")
    
    return {
        "id": file.id,
        "filename": file.filename,
        "file_type": file.file_type,
        "content": file.content
    }


@router.get("/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """Download a specific file"""
    file_repository = FileRepository(db)
    file = file_repository.find_by_id(file_id)
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file.status != "completed":
        raise HTTPException(status_code=400, detail="File is not ready for download")
    
    # Determine content type
    content_type_map = {
        "txt": "text/plain",
        "json": "application/json",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "md": "text/markdown",
    }
    content_type = content_type_map.get(file.file_type, "application/octet-stream")
    
    return Response(
        content=file.content.encode('utf-8'),
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{file.filename}"'
        }
    )


@router.get("/project/{project_id}/logs", response_model=List[LogResponse])
def get_generation_logs(project_id: int, db: Session = Depends(get_db)):
    """Get generation logs for a project"""
    log_repository = LogRepository(db)
    logs = log_repository.find_by_project_id(project_id)
    return logs


@router.get("/project/{project_id}/download-all")
def download_all_files(project_id: int, db: Session = Depends(get_db)):
    """Download all files for a project as a ZIP file"""
    file_repository = FileRepository(db)
    files = file_repository.find_by_project_id(project_id)
    
    # Filter only completed files
    completed_files = [file for file in files if file.status == "completed"]
    
    if not completed_files:
        raise HTTPException(status_code=404, detail="No completed files found for this project")
    
    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in completed_files:
            # Add file to ZIP with its filename
            zip_file.writestr(file.filename, file.content.encode('utf-8'))
    
    zip_buffer.seek(0)
    
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="project_{project_id}_files.zip"'
        }
    )

