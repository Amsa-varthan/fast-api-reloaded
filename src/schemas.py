# schemas.py
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
    emailVerified: bool
    accountStatus: str
    
    class Config:
        from_attributes = True

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
