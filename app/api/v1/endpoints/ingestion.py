# app/api/v1/endpoints/ingestion.py

from fastapi import APIRouter, UploadFile, File, Depends
from app.services.ingestion_service import process_file
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    result = await process_file(file, user.id)

    return {
        "message": "File processed successfully",
        "chunks_created": result
    }