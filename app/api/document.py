"""
Document API

Endpoints for uploading and getting all documents.
All routes require a valid JWT (get_current_user).
"""

from __future__ import annotations

import logging
import traceback
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from core.deps import get_current_user
from app.schemas.document_schema import DocumentOut
from app.services import document_service

router = APIRouter()


@router.post("/", response_model=DocumentOut, status_code=status.HTTP_200_OK)
async def upload_document(
    file: UploadFile = File(...),
    trip_id: int | None = Form(None),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Upload a travel document and persist its metadata.

    Returns:
        DocumentOut  JSON describing the stored document.
    """
    try:
        await document_service.validate_upload_file(file)

        return await document_service.save_document(
            db=db,
            user_id=user.id,
            trip_id=trip_id,
            file=file,
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve

    except Exception as exc:  
        logging.error("upload_document failed:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail="upload failed") from exc


@router.get("/", response_model=list[DocumentOut])
async def list_documents(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    trip_id: int | None = Query(None),
):
    """
    List all documents for the authenticated user.
    Optional trip filter.
    """
    return await document_service.get_all_documents(
        db=db,
        user_id=user.id,
        trip_id=trip_id,
    )
