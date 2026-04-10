# app/api/v1/endpoints/query.py

from fastapi import APIRouter, Depends
from app.services.query_service import query_knowledge
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/ask")
def ask(query: str, user = Depends(get_current_user)):
    response = query_knowledge(query, user.id)

    return {
        "query": query,
        "response": response
    }