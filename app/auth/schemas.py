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

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MessageResponse(BaseModel):
    message: str
