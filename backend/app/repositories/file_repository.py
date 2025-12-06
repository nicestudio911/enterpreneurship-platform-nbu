from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.generated_file import GeneratedFile


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_project_id(self, project_id: int) -> List[GeneratedFile]:
        return self.db.query(GeneratedFile).filter(GeneratedFile.project_id == project_id).all()

    def find_by_id(self, file_id: int) -> Optional[GeneratedFile]:
        return self.db.query(GeneratedFile).filter(GeneratedFile.id == file_id).first()

    def save(self, file: GeneratedFile) -> GeneratedFile:
        try:
            self.db.add(file)
            self.db.commit()
            self.db.refresh(file)
            return file
        except Exception:
            self.db.rollback()
            raise

    def delete(self, file: GeneratedFile) -> None:
        try:
            self.db.delete(file)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def delete_by_project_id(self, project_id: int) -> None:
        """Delete all files for a project"""
        try:
            deleted_count = self.db.query(GeneratedFile).filter(
                GeneratedFile.project_id == project_id
            ).delete(synchronize_session=False)
            self.db.commit()
            print(f"Deleted {deleted_count} files for project {project_id}")
        except Exception:
            self.db.rollback()
            raise

