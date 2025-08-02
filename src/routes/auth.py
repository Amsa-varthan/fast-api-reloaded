import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError # Import the exception
from datetime import datetime, timedelta

from database.database import get_db
from database.models.user import User, UserToken
from database.models.phone_verification import PhoneVerification
from src import schemas
from src.services import otp_service
from src.utils import security_utils
from config import settings

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# ... (verify-phone and verify-otp functions remain the same) ...

@router.post("/verify-phone", response_model=schemas.PhoneVerificationStartResponse)
def start_phone_verification(request: schemas.PhoneVerificationStartRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == request.phone).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"success": False, "error": "PHONE_EXISTS", "message": "Phone number already registered"}
        )
    otp = otp_service.generate_otp()
    session_id = f"sess_{uuid.uuid4().hex}"
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    new_session = PhoneVerification(
        session_id=session_id,
        phone=request.phone,
        session_type='signup',
        otp_hash=security_utils.hash_value(otp),
        expires_at=expires_at
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    print(f"OTP for {request.phone} is: {otp}")
    return schemas.PhoneVerificationStartResponse(
        data=schemas.PhoneVerificationStartResponseData(
            sessionId=session_id,
            phone=request.phone,
            otpExpiresAt=expires_at
        )
    )

@router.post("/verify-otp")
def verify_otp(request: schemas.OTPVerifyRequest, db: Session = Depends(get_db)):
    session = db.query(PhoneVerification).filter(PhoneVerification.session_id == request.sessionId).first()
    if not session or session.expires_at < datetime.utcnow() or session.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired session")
    if not security_utils.verify_hash(request.otp, session.otp_hash):
        session.attempts += 1
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    session.is_verified = True
    db.commit()
    return {"success": True, "message": "Phone verified successfully", "data": {"sessionId": session.session_id, "isVerified": True}}


@router.post("/complete-profile", response_model=schemas.AuthSuccessResponse)
def complete_profile(request: schemas.CompleteProfileRequest, db: Session = Depends(get_db)):
    session = db.query(PhoneVerification).filter(PhoneVerification.session_id == request.sessionId).first()
    if not session or not session.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Session not verified")

    new_user = User(
        name=request.name,
        phone=session.phone,
        is_phone_verified=True,
        email=request.email,
        address=request.address.model_dump()
    )
    db.add(new_user)
    
    # --- ADDED ERROR HANDLING ---
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"success": False, "error": "USER_ALREADY_EXISTS", "message": "A user with this phone number or email already exists."}
        )
    # --------------------------

    db.refresh(new_user)
    access_token = security_utils.create_access_token(data={"sub": str(new_user.id)})
    refresh_token_str, refresh_token_hash = security_utils.create_refresh_token()
    new_refresh_token = UserToken(
        user_id=new_user.id,
        refresh_token_hash=refresh_token_hash,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(new_refresh_token)
    db.commit()

    return schemas.AuthSuccessResponse(
        message="Account created successfully",
        data=schemas.TokenData(
            accessToken=access_token,
            refreshToken=refresh_token_str,
            user=schemas.UserSchema.from_orm(new_user)
        )
    )
