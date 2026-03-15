from pydantic import BaseModel
from datetime import datetime

class CmsPageBase(BaseModel):
    title: str
    content: str

class CmsPageRead(CmsPageBase):
    id: int
    slug: str
    updated_at: datetime

    class Config:
        from_attributes = True

class CmsPageUpdate(BaseModel):
    content: str
