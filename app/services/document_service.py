"""
Document Service

Provides business logic for creating, fetching, and deleting documents.
Interacts with the repository layer and handles data transformation.
"""

import os
from io import BytesIO
from fastapi import UploadFile, HTTPException
from app.models.document import TravelDocument
from app.repositories import document_repository
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.s3_storage import S3FileStorage
from infrastructure.local_storage import LocalFileStorage

UPLOAD_DIR = "uploaded_docs" 

USE_S3 = os.getenv("USE_S3", "false").lower() == "true"
storage_backend = S3FileStorage() if USE_S3 else LocalFileStorage()

async def save_document(
    db: AsyncSession,
    user_id: int,
    trip_id: int | None,
    file: UploadFile
) -> TravelDocument:
    """
    Save uploaded file to configured storage and store metadata.

    Args:
        db (AsyncSession): DB session
        user_id (int): Authenticated user
        trip_id (Optional[int]): Trip association
        file (UploadFile): Uploaded file

    Returns:
        TravelDocument: ORM record
    """
    file_url = await storage_backend.upload(file, file.filename)

    doc = TravelDocument(
        user_id=user_id,
        trip_id=trip_id,
        file_name=file.filename,
        file_path=file_url,
    )

    return await document_repository.create(db, doc)

async def get_all_documents(
    db: AsyncSession, user_id: int, trip_id: Optional[int] = None
) -> List[TravelDocument]:
    """
    Service function to retrieve all uploaded documents for a user,
    optionally filtered by trip_id.
    """
    return await document_repository.get_all_documents(db, user_id, trip_id)

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
MAX_FILE_SIZE_MB = 5

async def validate_upload_file(file: UploadFile):
    """
    Validates file extension and size before saving.
    Rewinds file pointer after reading.
    """
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5MB size limit.")

    file.file.seek(0)  # Rewind so it can be read during upload
    return file
