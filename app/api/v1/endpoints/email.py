# app/api/v1/endpoints/email.py

from fastapi import APIRouter, Depends
from app.services.email_service import generate_email
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/generate")
def generate_email_api(task: str, user = Depends(get_current_user)):
    response = generate_email(task, user.id)

    return {
        "task": task,
        "email": response
    }