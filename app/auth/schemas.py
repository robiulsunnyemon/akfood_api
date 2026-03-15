from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SignUpRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    district: str
    city: str
    address: str
    password: str = Field(min_length=6)
    confirm_password: str

class LoginRequest(BaseModel):
    email_or_phone: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp_code: str = Field(min_length=6, max_length=6)

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str = Field(min_length=6)
    confirm_password: str

class ProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6)
    confirm_new_password: str

class DeleteAccountRequest(BaseModel):
    password: str

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    profile_img_url: Optional[str] = None
    role: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

class MessageResponse(BaseModel):
    message: str

class GoogleLoginRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    id_token: str
