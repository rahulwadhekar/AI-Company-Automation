# app/api/v1/endpoints/agent.py

from fastapi import APIRouter, Depends
from app.services.agent_service import run_smart_agent
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/run")
def run_agent_api(task: str, user = Depends(get_current_user)):
    response = run_smart_agent(task, user.id)

    return {
        "task": task,
        "result": response
    }