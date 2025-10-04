# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str

# Study Session
class StudySessionCreate(BaseModel):
    title: str
    subject: Optional[str]
    datetime: Optional[datetime]
    duration_mins: Optional[int]
    notes: Optional[str]
    status: Optional[str] = "todo"

class StudySessionOut(StudySessionCreate):
    id: str
    plan_id: Optional[str]

    class Config:
        orm_mode = True

# Study Plan
class StudyPlanCreate(BaseModel):
    title: str
    subject_tags: Optional[List[str]] = []
    start_date: Optional[datetime]
    end_date: Optional[datetime]

class StudyPlanOut(BaseModel):
    id: str
    title: str
    subject_tags: Optional[List[str]]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_by: str
    sessions: List[StudySessionOut] = []

    class Config:
        orm_mode = True
