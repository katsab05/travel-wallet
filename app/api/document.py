"""
Document API .

Defines endpoint for uploading user/trip documents.
All routes are protected by OAuth2 token-based authentication.
"""

from fastapi import APIRouter, UploadFile, File, Form, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from core.deps import get_current_user
from app.services import document_service
from app.schemas.document_schema import DocumentOut

router = APIRouter()

@router.post("/", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...),
    trip_id: int = Form(None),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Endpoint to upload a travel document.

    Saves the uploaded file and its metadata (file name, path, associated user/trip) to the database.

    Args:
        file (UploadFile): The file being uploaded (e.g. PDF, image)
        trip_id (int): Optional ID of the associated trip
        db (AsyncSession): Dependency-injected DB session
        user: Currently authenticated user

    Returns:
        DocumentOut: Metadata of the uploaded document
    """
    # validate extension and file size
    await document_service.validate_upload_file(file)

    return await document_service.save_document(
        db=db,
        user_id=user.id,
        trip_id=trip_id,
        file=file
    )

@router.get("/", response_model=list[DocumentOut])
async def get_all_documents(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    trip_id: int = Query(default=None)
):
    """
    List all uploaded documents for the user.
    Optionally filter by trip ID.
    """
    return await document_service.get_all_documents(db, user.id, trip_id)
