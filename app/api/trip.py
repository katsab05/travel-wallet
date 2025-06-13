"""
Trip API

Endpoints for listing, creating, and deleting trips.
All routes require a valid JWT (get_current_user).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from core.deps import get_current_user
from app.schemas.trip_schema import TripIn, TripOut
from app.services import trip_service

router = APIRouter()


# ──────────────────────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────────────────────
@router.post(
    "/", 
    response_model=TripOut, 
    status_code=status.HTTP_201_CREATED
)
async def create_trip(
    trip_in: TripIn,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),           # ✅ auth
):
    """
    Create a new trip for the authenticated user.
    FastAPI will serialize the returned ORM object → TripOut.
    """
    trip = await trip_service.create_trip_service(
        db=db,
        trip_data=trip_in,
        user_id=user.id,
    )
    return trip                                  # ORM ➜ TripOut via orm_mode


# ──────────────────────────────────────────────────────────
# LIST
# ──────────────────────────────────────────────────────────
@router.get("/", response_model=list[TripOut])
async def get_all_trips(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    """
    List all trips belonging to the authenticated user.
    """
    return await trip_service.get_all_trips_service(db, user_id=user.id)


# ──────────────────────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────────────────────
@router.delete("/{trip_id}", status_code=status.HTTP_200_OK)
async def delete_trip(
    trip_id: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    """
    Delete a trip the user owns.
    """
    ok = await trip_service.delete_trip_service(db, trip_id, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"status": "deleted"}
