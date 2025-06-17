"""
Document Service
────────────────
Business rules for saving / listing documents.

• Chooses S3 or local backend based on USE_S3 env var.
• Validates file type & size.
"""

from __future__ import annotations
import os
from typing import Optional, List

from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import TravelDocument
from app.repositories import document_repository
from infrastructure.s3_storage import S3FileStorage
from infrastructure.local_storage import LocalFileStorage

# Config
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
MAX_FILE_SIZE_MB = 5

USE_S3 = os.getenv("USE_S3", "false").lower() == "true"
storage_backend = S3FileStorage() if USE_S3 else LocalFileStorage()

# Validation
async def validate_upload_file(file: UploadFile) -> None:
    """
    Raises HTTP 400 on unsupported extension or >5 MB size.
    Rewinds pointer afterwards.
    """
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5 MB size limit.")

    file.file.seek(0) 

# Service Func
async def save_document(
    db: AsyncSession,
    user_id: int,
    trip_id: int | None,
    file: UploadFile,
) -> TravelDocument:
    """
    • Validates file
    • Uploads to chosen backend
    • Persists metadata row
    • Returns ORM object
    """
    await validate_upload_file(file)

    try:
        file_url = await storage_backend.upload(file, file.filename)
    except Exception as exc: 
       
        import logging, traceback
        logging.error("Storage backend failed:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail="upload failed") from exc

    doc = TravelDocument(
        user_id=user_id,
        trip_id=trip_id,
        file_name=file.filename,
        file_path=file_url,
    )
    return await document_repository.create(db, doc)


async def get_all_documents(
    db: AsyncSession,
    user_id: int,
    trip_id: Optional[int] = None,
) -> List[TravelDocument]:
    """Return all docs for user, optional trip filter."""
    return await document_repository.get_all_documents(db, user_id, trip_id)
