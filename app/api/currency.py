from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import currency_service
from app.db import session

router = APIRouter()

@router.get("/convert")
async def convert(
    amount: float = Query(...),
    from_currency: str = Query(...),
    to_currency: str = Query(default="USD"),
    db: AsyncSession = Depends(session.get_db)
):
    """
    Convert currency using live exchange rates.
    """
    result = await currency_service.convert_currency(amount, from_currency, to_currency, db)
    return {"converted_amount": round(result, 2)}



