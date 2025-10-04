# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from database import create_db_and_tables, get_session
from sqlmodel import Session, select
from schemas import UserCreate, UserOut, Token, StudyPlanCreate, StudyPlanOut, StudySessionCreate, StudySessionOut
from crud import create_user, authenticate_user, create_plan, get_plans_for_user, get_plan_by_id, add_session_to_plan, update_session, delete_session
from auth import create_access_token, get_current_user
from models import User, StudyPlan, StudySession
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Study Buddy Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Register
@app.post("/register", response_model=UserOut)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == user_in.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    user = create_user(session, user_in.username, user_in.email, user_in.password)
    return user

# Token
@app.post("/token", response_model=Token)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
@app.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

# Plans
@app.post("/plans", response_model=StudyPlanOut)
def create_plan_endpoint(plan_in: StudyPlanCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    plan = create_plan(session, plan_in.title, plan_in.subject_tags or [], created_by=current_user.id, start_date=plan_in.start_date, end_date=plan_in.end_date)
    out = StudyPlanOut.from_orm(plan)
    out.subject_tags = plan.subject_tags.split(",") if plan.subject_tags else []
    return out

@app.get("/plans", response_model=List[StudyPlanOut])
def list_plans(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    plans = get_plans_for_user(session, current_user.id)
    out = []
    for p in plans:
        p_out = StudyPlanOut.from_orm(p)
        p_out.subject_tags = p.subject_tags.split(",") if p.subject_tags else []
        sessions = session.exec(select(StudySession).where(StudySession.plan_id == p.id)).all()
        p_out.sessions = [StudySessionOut.from_orm(s) for s in sessions]
        out.append(p_out)
    return out
