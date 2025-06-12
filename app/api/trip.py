from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.trip_schema import TripIn, TripOut
from app.repositories.trip_repository import *
from app.db.session import get_db
from app.models.trip import Trip

router = APIRouter()

@router.post("/", response_model=TripOut)
async def create(trip_data: TripIn, db: AsyncSession = Depends(get_db)):
    trip = Trip(**trip_data.dict())
    return await create_trip(db, trip)

@router.get("/", response_model=list[TripOut])
async def list_all(db: AsyncSession = Depends(get_db)):
    return await list_trips(db)

@router.delete("/{trip_id}")
async def delete(trip_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_trip(db, trip_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"status": "deleted"}
