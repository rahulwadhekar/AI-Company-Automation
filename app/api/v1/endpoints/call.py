# app/api/v1/endpoints/call.py

from fastapi import APIRouter, Depends
from app.services.call_service import generate_call_script
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/generate")
def generate_call_api(task: str, user = Depends(get_current_user)):
    response = generate_call_script(task, user.id)

    return {
        "task": task,
        "call_script": response
    }