from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class APICreate(BaseModel):
    name: str
    url: str
    method: str = "GET"
    description: Optional[str] = None
    category: str = "General"

class APIUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class APIResponse(BaseModel):
    id: int
    name: str
    url: str
    method: str
    description: Optional[str]
    category: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
