"""
Trip API Router.

Defines endpoints for listing, creating, and deleting trips.
All routes are protected by OAuth2 token-based authentication.
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.trip_schema import TripIn, TripOut
from app.repositories.trip_repository import *
from app.db.session import get_db
from app.models.trip import Trip
from core.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=TripOut)
async def create(trip_data: TripIn, db: AsyncSession = Depends(get_db)):
    """
    Create a new trip record.
    """
    trip = Trip(**trip_data.dict())
    return await create_trip(db, trip)

@router.get("/", response_model=list[TripOut])
async def list_all(db: AsyncSession = Depends(get_db), user=Depends(get_current_user) ):
    """
    List all trips for the authenticated user.
    """
    return await list_trips(db)

@router.delete("/{trip_id}")
async def delete(trip_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a specific trip by trip ID.
    """
    ok = await delete_trip(db, trip_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"status": "deleted"}
