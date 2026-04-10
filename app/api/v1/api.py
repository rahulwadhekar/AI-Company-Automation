from fastapi import APIRouter
from app.api.v1.endpoints import auth, query, ingestion, email, call, agent


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["Ingestion"])
api_router.include_router(query.router, prefix="/query", tags=["Query"])
api_router.include_router(email.router, prefix="/email", tags=["Email"])
api_router.include_router(call.router, prefix="/call", tags=["Call"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])


