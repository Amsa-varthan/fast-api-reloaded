from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from database.database import get_db
from database.models.user import User
from database.models.jobs import Job
from src import schemas
from src.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post("/", response_model=schemas.JobSchema, status_code=status.HTTP_201_CREATED)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # In a real app, you might want to verify the user is a recruiter
    new_job = Job(**job.model_dump(), recruiter_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=list[schemas.JobSchema])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.status == 'open').all()
    return jobs
