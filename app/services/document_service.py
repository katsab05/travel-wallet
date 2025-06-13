"""
Document Service

Provides business logic for creating, fetching, and deleting documents.
Interacts with the repository layer and handles data transformation.
"""

import os
from fastapi import UploadFile
from app.models.document import TravelDocument
from app.repositories import document_repository
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.s3_storage import MockS3Storage
from infrastructure.local_storage import LocalFileStorage

UPLOAD_DIR = "uploaded_docs" 

USE_S3 = os.getenv("USE_S3", "false").lower() == "true"
storage_backend = MockS3Storage() if USE_S3 else LocalFileStorage()

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
