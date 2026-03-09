from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    profile_img_url: Optional[str] = None
    is_active: bool

class UserUpdateProfileRequest(BaseModel):
    name: str # From the UI wireframe, a single Name field
    phone_number: str
    email: EmailStr
    district: str
    city: str
    address: str
