import uuid
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Schemas for Phone Verification
class PhoneVerificationStartRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\+91[6-9]\d{9}$")

class PhoneVerificationStartResponseData(BaseModel):
    sessionId: str
    phone: str
    otpExpiresAt: datetime

class PhoneVerificationStartResponse(BaseModel):
    success: bool = True
    message: str = "OTP sent successfully"
    data: PhoneVerificationStartResponseData

# Schemas for OTP Verification
class OTPVerifyRequest(BaseModel):
    sessionId: str
    otp: str = Field(..., min_length=6, max_length=6)

# Schemas for Profile Completion
class AddressSchema(BaseModel):
    street: str
    city: str
    state: str
    pincode: str
    country: str = "India"

class CompleteProfileRequest(BaseModel):
    sessionId: str
    name: str
    address: AddressSchema
    email: EmailStr | None = None

# Schemas for User and Tokens
class UserSchema(BaseModel):
    id: uuid.UUID
    phone: str
    name: str
    email: EmailStr | None = None
    # This field will now correctly map from the 'is_email_verified' model attribute
    emailVerified: bool = Field(..., alias='is_email_verified')
    # This field will now correctly map from the 'account_status' model attribute
    accountStatus: str = Field(..., alias='account_status')
    
    class Config:
        from_attributes = True
        # Add this to allow population by field name OR alias
        populate_by_name = True


class TokenData(BaseModel):
    accessToken: str
    refreshToken: str
    user: UserSchema

class AuthSuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: TokenData

# Schema for Refresh Token
class RefreshTokenRequest(BaseModel):
    refreshToken: str

# Schemas for Jobs
class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    job_type: str | None = None
    experience_level: str | None = None

class JobCreate(JobBase):
    pass

class JobSchema(JobBase):
    id: uuid.UUID
    recruiter_id: uuid.UUID
    posted_date: datetime
    status: str

    class Config:
        from_attributes = True

# Schemas for Applications
class ApplicationCreate(BaseModel):
    resume_url: str
    cover_letter: str | None = None

class ApplicationSchema(ApplicationCreate):
    id: uuid.UUID
    job_id: uuid.UUID
    candidate_id: uuid.UUID
    applied_date: datetime
    status: str
    job: JobSchema # Include job details in the response
    candidate: UserSchema # Include candidate details

    class Config:
        from_attributes = True
