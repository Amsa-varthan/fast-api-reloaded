import uuid
from sqlalchemy import Column, String, Integer, DateTime, func, Enum, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database import Base

JobStatus = Enum('open', 'closed', 'archived', name='job_status')
ApplicationStatus = Enum('pending', 'reviewed', 'shortlisted', 'rejected', name='application_status')
JobType = Enum('full-time', 'part-time', 'contract', 'internship', name='job_type')
ExperienceLevel = Enum('entry-level', 'mid-level', 'senior-level', 'executive', name='experience_level')

class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    job_type = Column(JobType)
    experience_level = Column(ExperienceLevel)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    posted_date = Column(DateTime, default=func.now())
    status = Column(JobStatus, default='open', nullable=False)
    recruiter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    recruiter = relationship("User")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    # The fields below would be used if non-registered users could apply
    # For this example, we link directly to the candidate's user profile
    # candidate_name = Column(String(100), nullable=False)
    # candidate_email = Column(String(255), nullable=False)
    resume_url = Column(String(255)) # URL to a stored resume file
    cover_letter = Column(Text)
    applied_date = Column(DateTime, default=func.now())
    status = Column(ApplicationStatus, default='pending', nullable=False)

    job = relationship("Job", back_populates="applications")
    candidate = relationship("User")
