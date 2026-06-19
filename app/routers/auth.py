from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import get_db
from app.schemas.user import (
    UserCreate, UserLogin, UserOut, Token,
    ForgotPasswordPayload, ResetPasswordPayload,
    VerifyEmailPayload, MessageResponse
)
from app.models.user import User
from app.core.security import (
    hash_password, verify_password, create_access_token,
    create_reset_token, create_verification_token, decode_token
)
from app.core.dependencies import get_current_user
from app.core.email import send_email
from app.config import settings

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_verification_token(new_user.id)
    verify_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    try:
        await send_email(
            subject="Verify your Tayora Sustain account",
            recipients=[new_user.email],
            body=f"<p>Welcome to Tayora Sustain! Click below to verify your account:</p><a href='{verify_link}'>Verify Email</a>"
        )
    except Exception:
        pass

    return new_user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id), "role": user.role})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=1800
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "user": user
    }


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="none"
    )
    return {"message": "Logged out successfully"}


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(payload: ForgotPasswordPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    token = create_reset_token(user.id)
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    try:
        await send_email(
            subject="Reset your Tayora Sustain password",
            recipients=[user.email],
            body=f"<p>Click below to reset your password. This link expires in 30 minutes.</p><a href='{reset_link}'>Reset Password</a>"
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send email")

    return {"message": "Password reset link sent to your email"}


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordPayload, db: Session = Depends(get_db)):
    try:
        decoded = decode_token(payload.token)
        if decoded.get("type") != "reset":
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        user_id = decoded.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(payload.new_password)
    db.commit()

    return {"message": "Password reset successful"}


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(payload: VerifyEmailPayload, db: Session = Depends(get_db)):
    try:
        decoded = decode_token(payload.token)
        if decoded.get("type") != "verify":
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        user_id = decoded.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()

    return {"message": "Email verified successfully"}


@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification(payload: ForgotPasswordPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    if user.is_verified:
        return {"message": "Email is already verified"}

    token = create_verification_token(user.id)
    verify_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    try:
        await send_email(
            subject="Verify your Tayora Sustain account",
            recipients=[user.email],
            body=f"<p>Click below to verify your account:</p><a href='{verify_link}'>Verify Email</a>"
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send email")

    return {"message": "Verification email resent"}