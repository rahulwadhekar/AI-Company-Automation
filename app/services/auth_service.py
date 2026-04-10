from sqlalchemy.orm import Session
from app.repositories import user_repo
from app.utils.hash import hash_password, verify_password
from app.core.security import create_access_token
from fastapi import HTTPException

def register(db: Session, email: str, password: str):
    hashed = hash_password(password)
    user = user_repo.create_user(db, email, hashed)
    return user

def login(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)

    print(f"🔍 Attempting login for email: {email}")
    print(f"👤 User found: {user is not None}")

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})

    return token