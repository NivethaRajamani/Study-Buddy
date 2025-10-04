# backend/models.py
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# ID generator
def gen_id(prefix: str) -> str:
    import uuid
    return f"{prefix}{uuid.uuid4().hex[:8]}"

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: gen_id("user_"), primary_key=True)
    username: str
    email: str
    password: str

    # Relationships
    study_plans: List["StudyPlan"] = Relationship(back_populates="user")

class StudyPlan(SQLModel, table=True):
    id: str = Field(default_factory=lambda: gen_id("plan_"), primary_key=True)
    title: str
    subject_tags: Optional[str] = None  # comma-separated tags
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    created_by: str = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="study_plans")
    sessions: List["StudySession"] = Relationship(back_populates="plan")

class StudySession(SQLModel, table=True):
    id: str = Field(default_factory=lambda: gen_id("sess_"), primary_key=True)
    title: str
    subject: Optional[str] = None
    datetime_: Optional[datetime] = Field(default=None, alias="datetime")
    duration_mins: Optional[int] = None
    notes: Optional[str] = None
    status: str = Field(default="todo")

    plan_id: Optional[str] = Field(default=None, foreign_key="studyplan.id")
    plan: Optional[StudyPlan] = Relationship(back_populates="sessions")
