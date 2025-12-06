from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models.competition import Competition

router = APIRouter(prefix="/api/competitions", tags=["competitions"])


class CompetitionResponse(BaseModel):
    id: int
    name: str
    description: str | None
    advice_prompt: str | None
    file_generation_prompt: str | None
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=List[CompetitionResponse])
def get_all_competitions(db: Session = Depends(get_db)):
    """Get all available competitions"""
    competitions = db.query(Competition).all()
    return competitions


@router.get("/{competition_id}", response_model=CompetitionResponse)
def get_competition(competition_id: int, db: Session = Depends(get_db)):
    """Get a specific competition by ID"""
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if not competition:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition

