import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base

SessionType = Enum('signup', 'login', name='session_type')

class PhoneVerification(Base):
    __tablename__ = "phone_verification"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    session_type = Column(SessionType, nullable=False)
    is_verified = Column(Boolean, default=False)
    otp_hash = Column(String, nullable=False)
    attempts = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
