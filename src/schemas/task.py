from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: int = Field(default=0, ge=0, le=5)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[int] = Field(None, ge=0, le=5)
    done: Optional[bool] = False


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    done: bool
    created_at: Optional[datetime] = None 


    class Config:
        from_attributes = True  # Allows mapping from SQLAlchemy model