"""
Trip API Router.

Defines endpoints for listing, creating, and deleting trips.
All routes are protected by OAuth2 token-based authentication.
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.trip_schema import TripIn, TripOut
from app.repositories.trip_repository import *
from app.services import trip_service
from app.db.session import get_db
from app.models.trip import Trip
from core.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=TripOut)
async def create_trip(trip_data: TripIn, db: AsyncSession = Depends(get_db)):
    """
    Create a new trip record.
    """
    trip = Trip(**trip_data.dict())
    return await trip_service.create_trip_service(db, trip)

@router.get("/", response_model=list[TripOut])
async def get_all_trips(db: AsyncSession = Depends(get_db), user=Depends(get_current_user) ):
    """
    List all trips for the authenticated user.
    """
    return await trip_service.get_all_trips_service(db)

@router.delete_trip("/{trip_id}")
async def delete_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a specific trip by trip ID.
    """
    ok = await trip_service.delete_trip_service(db, trip_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"status": "deleted"}
