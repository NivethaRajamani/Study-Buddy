# backend/crud.py
from sqlmodel import Session, select
from models import User, StudyPlan, StudySession
from auth import get_password_hash, verify_password
from typing import Optional, List

# User
def create_user(session: Session, username: str, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# Study Plan
def create_plan(session: Session, title: str, subject_tags: List[str], created_by: str, start_date=None, end_date=None) -> StudyPlan:
    plan = StudyPlan(
        title=title,
        subject_tags=",".join(subject_tags),
        created_by=created_by,
        start_date=start_date,
        end_date=end_date
    )
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

def get_plans_for_user(session: Session, user_id: str) -> List[StudyPlan]:
    return session.exec(select(StudyPlan).where(StudyPlan.created_by == user_id)).all()

def get_plan_by_id(session: Session, plan_id: str) -> Optional[StudyPlan]:
    return session.get(StudyPlan, plan_id)

# Study Session
def add_session_to_plan(session: Session, plan_id: str, data: dict) -> StudySession:
    s = StudySession(plan_id=plan_id, **data)
    session.add(s)
    session.commit()
    session.refresh(s)
    return s

def update_session(session: Session, session_id: str, data: dict) -> StudySession:
    s = session.get(StudySession, session_id)
    for key, value in data.items():
        setattr(s, key, value)
    session.add(s)
    session.commit()
    session.refresh(s)
    return s

def delete_session(session: Session, session_id: str) -> bool:
    s = session.get(StudySession, session_id)
    if not s:
        return False
    session.delete(s)
    session.commit()
    return True
