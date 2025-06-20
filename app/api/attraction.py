from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.attraction_schema import AttractionOut
from app.db.session import get_db
from app.services.attraction_service import AttractionService

router = APIRouter()


@router.get("/", response_model=List[AttractionOut])
async def get_local_attractions(db: AsyncSession = Depends(get_db)):
    service = AttractionService(db)
    return await service.list_local_attractions()


@router.post("/discover", response_model=List[AttractionOut])
async def discover_nearby_attractions(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = AttractionService(db)
        return await service.fetch_and_store_nearby_attractions(lat=lat, lon=lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
