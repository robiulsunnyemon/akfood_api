from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from pydantic import EmailStr
import random
import string
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db import db
from app.config.settings import settings
from app.utils.email import send_otp_email
from .schemas import (
    SignUpRequest,
    LoginRequest,
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest,
    ProfileUpdateRequest,
    DeleteAccountRequest,
    TokenResponse,
    UserRead,
    MessageResponse,
    GoogleLoginRequest,
    ChangePasswordRequest
)
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.jwt_expire_days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def generate_otp() -> str:
    return ''.join(random.choices(string.digits, k=6))

async def signup(user_data: SignUpRequest) -> TokenResponse:
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    # Check if user exists
    existing_user = await db.user.find_first(
        where={
            "OR": [
                {"email": user_data.email},
                {"phone_number": {"equals": user_data.phone_number}}
            ]
        }
    )
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or phone number already exists")

    hashed_pw = get_password_hash(user_data.password)
    new_user = await db.user.create(
        data={
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "phone_number": user_data.phone_number,
            "district": user_data.district,
            "city": user_data.city,
            "address": user_data.address,
            "hashed_password": hashed_pw
        }
    )

    access_token = create_access_token(data={"sub": str(new_user.id)})
    return TokenResponse(access_token=access_token, user=new_user)

async def login(login_data: LoginRequest) -> TokenResponse:
    user = await db.user.find_first(
        where={
            "OR": [
                {"email": login_data.email_or_phone},
                {"phone_number": {"equals": login_data.email_or_phone}}
            ]
        }
    )
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, user=user)

async def forgot_password(data: ForgotPasswordRequest) -> MessageResponse:
    user = await db.user.find_unique(where={"email": data.email})
    if not user:
        # We still return success to not leak email existence
        return MessageResponse(message="If this email is registered, you will receive an OTP.")

    otp_code = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expire_minutes)
    
    # Store OTP
    await db.otp.create(
        data={
            "email": data.email,
            "otp_code": otp_code,
            "expires_at": expires_at
        }
    )
    
    # Send real email using fastapi-mail
    await send_otp_email(email=data.email, otp=otp_code)
    
    return MessageResponse(message="OTP generated and sent successfully.")

async def verify_otp(data: VerifyOTPRequest) -> TokenResponse:
    # Find OTP
    otp_record = await db.otp.find_first(
        where={
            "email": data.email,
            "otp_code": data.otp_code,
            "expires_at": {"gt": datetime.now(timezone.utc)}
        },
        order={"created_at": "desc"}
    )
    
    if not otp_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")
    
    # OPTIONAL: You could delete the OTP immediately to prevent reuse
    # Or keep it until password reset finishes. Let's issue a temporary token.
    user = await db.user.find_unique(where={"email": data.email})
    reset_token = create_access_token(data={"sub": data.email, "type": "password_reset"}, expires_delta=timedelta(minutes=15))
    return TokenResponse(access_token=reset_token, user=user)

async def reset_password(data: ResetPasswordRequest) -> MessageResponse:
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    try:
        payload = jwt.decode(data.reset_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if email is None or token_type != "password_reset":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid reset token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid reset token")
    
    user = await db.user.find_unique(where={"email": email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    hashed_pw = get_password_hash(data.new_password)
    
    await db.user.update(
        where={"email": email},
        data={"hashed_password": hashed_pw}
    )
    
    # Delete all OTPs for this email to clean up
    await db.otp.delete_many(where={"email": email})
    
    return MessageResponse(message="Password reset successfully")

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id_str: str = payload.get("sub")
        if user_id_str is None or "type" in payload:  # Make sure we don't accidentally auth with reset_token
            raise credentials_exception
        user_id = int(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exception
        
    user = await db.user.find_unique(where={"id": user_id})
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

async def get_admin_user(current_user = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to perform this action"
        )
    return current_user

async def google_login(data: GoogleLoginRequest) -> TokenResponse:
    # In a real app, you'd verify the id_token here
    # try:
    #     idinfo = id_token.verify_oauth2_token(data.id_token, google_requests.Request(), settings.google_client_id)
    #     if idinfo['email'] != data.email:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token email")
    # except ValueError:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid google token")

    # Check if user exists
    user = await db.user.find_unique(where={"email": data.email})
    
    if not user:
        # Create new user
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        hashed_pw = get_password_hash(random_password)
        user = await db.user.create(
            data={
                "first_name": data.first_name,
                "last_name": data.last_name,
                "email": data.email,
                "hashed_password": hashed_pw,
                # Other fields can be updated later by the user
            }
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, user=user)

async def update_profile(user_id: int, data: ProfileUpdateRequest) -> UserRead:
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        user = await db.user.find_unique(where={"id": user_id})
        return user
        
    updated_user = await db.user.update(
        where={"id": user_id},
        data=update_data
    )
    return updated_user

async def delete_account(user_id: int, data: DeleteAccountRequest) -> MessageResponse:
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        
    # Option 1: Deactivate account (soft delete)
    # await db.user.update(where={"id": user_id}, data={"is_active": False})
    
    # Option 2: Permanent deletion (requested "permanently Delete your account" in screenshot)
    await db.user.delete(where={"id": user_id})
    
    return MessageResponse(message="Account deleted successfully")

async def update_profile_image(user_id: int, image_url: str) -> UserRead:
    updated_user = await db.user.update(
        where={"id": user_id},
        data={"profile_img_url": image_url}
    )
    return updated_user

async def change_password(user_id: int, data: ChangePasswordRequest) -> MessageResponse:
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
        
    if data.new_password != data.confirm_new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New passwords do not match")
        
    hashed_pw = get_password_hash(data.new_password)
    await db.user.update(
        where={"id": user_id},
        data={"hashed_password": hashed_pw}
    )
    
    return MessageResponse(message="Password changed successfully")

