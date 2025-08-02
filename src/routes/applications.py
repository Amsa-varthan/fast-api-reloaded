from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from database.database import get_db
from database.models.user import User
from database.models.jobs import Job, Application
from src import schemas
from src.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

@router.post("/jobs/{job_id}/apply", response_model=schemas.ApplicationSchema, status_code=status.HTTP_201_CREATED)
def apply_for_job(job_id: uuid.UUID, application: schemas.ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id, Job.status == 'open').first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found or is closed")

    existing_application = db.query(Application).filter(Application.job_id == job_id, Application.candidate_id == current_user.id).first()
    if existing_application:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already applied for this job")

    new_application = Application(
        **application.model_dump(),
        job_id=job_id,
        candidate_id=current_user.id
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

@router.get("/my", response_model=list[schemas.ApplicationSchema])
def get_my_applications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """For Job Seekers: Get all applications submitted by the current user."""
    applications = db.query(Application).filter(Application.candidate_id == current_user.id).all()
    return applications

@router.get("/received", response_model=list[schemas.ApplicationSchema])
def get_received_applications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """For Recruiters: Get all applications for jobs posted by the current user."""
    applications = db.query(Application).join(Job).filter(Job.recruiter_id == current_user.id).all()
    return applications
