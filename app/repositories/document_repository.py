"""
Document Repository

Provides direct database access functions for Document model.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import TravelDocument

async def create(db: AsyncSession, doc: TravelDocument) -> TravelDocument:
    """
    Inserts a new TravelDocument record into the database.

    Args:
        db (AsyncSession): Active DB session
        doc (TravelDocument): ORM instance to be saved

    Returns:
        TravelDocument: Saved document with ID and timestamp
    """

    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc
