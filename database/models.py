# models.py
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

# Corrected import (removed the dot)
from database import Base

# Define ENUM types for account status and session type
AccountStatus = Enum('active', 'suspended', 'deleted', name='account_status')
SessionType = Enum('signup', 'login', name='session_type')

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    is_phone_verified = Column(Boolean, default=False)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    is_email_verified = Column(Boolean, default=False)
    address = Column(JSON, nullable=False)
    account_status = Column(AccountStatus, default='active', nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime, nullable=True)

    tokens = relationship("UserToken", back_populates="user")

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

class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    refresh_token_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="tokens")
