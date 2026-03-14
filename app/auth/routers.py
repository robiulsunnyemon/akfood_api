from fastapi import APIRouter, status, Depends
from . import schemas, service
from .service import get_current_user

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

@router.post("/google-login", response_model=schemas.TokenResponse, status_code=status.HTTP_200_OK)
async def google_login(data: schemas.GoogleLoginRequest):
    """Google Login / Instant Registration"""
    return await service.google_login(data)

@router.get("/me", response_model=schemas.UserRead)
async def get_me(current_user=Depends(get_current_user)):
    """Get current logged in user details"""
    return current_user

@router.put("/profile", response_model=schemas.UserRead)
async def update_profile(data: schemas.ProfileUpdateRequest, current_user=Depends(get_current_user)):
    """Update current user profile"""
    return await service.update_profile(current_user.id, data)

@router.delete("/account", response_model=schemas.MessageResponse)
async def delete_account(data: schemas.DeleteAccountRequest, current_user=Depends(get_current_user)):
    """Permanently delete user account"""
    return await service.delete_account(current_user.id, data)
