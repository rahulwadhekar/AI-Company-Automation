from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserLogin
from app.services import auth_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(db, user.email, user.password)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = auth_service.login(db, user.email, user.password)

    return {
        "access_token": token,
        "token_type": "bearer"
    }