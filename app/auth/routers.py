from fastapi import APIRouter, status
from . import schemas, service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: schemas.SignUpRequest):
    """Register a new user account"""
    return await service.signup(user_data)

@router.post("/login", response_model=schemas.TokenResponse, status_code=status.HTTP_200_OK)
async def login(login_data: schemas.LoginRequest):
    """Login with email or phone number"""
    return await service.login(login_data)

@router.post("/forgot-password", response_model=schemas.MessageResponse, status_code=status.HTTP_200_OK)
async def forgot_password(data: schemas.ForgotPasswordRequest):
    """Request a password reset OTP"""
    return await service.forgot_password(data)

@router.post("/verify-otp", response_model=schemas.TokenResponse, status_code=status.HTTP_200_OK)
async def verify_otp(data: schemas.VerifyOTPRequest):
    """Verify OTP and receive a temporary reset token"""
    return await service.verify_otp(data)

@router.post("/reset-password", response_model=schemas.MessageResponse, status_code=status.HTTP_200_OK)
async def reset_password(data: schemas.ResetPasswordRequest):
    """Reset password using the temporary reset token"""
    return await service.reset_password(data)
