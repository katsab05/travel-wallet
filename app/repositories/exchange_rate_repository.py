"""
Exchange-Rate Repository

Direct DB access helpers for the ExchangeRateCache model.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.exhange_rate_cache import ExchangeRateCache  

# Cache is considered fresh for 24 hours
CACHE_DURATION = timedelta(hours=24)


async def get_cached_rates(
    db: AsyncSession, base_currency: str
) -> Optional[Dict[str, float]]:
    """
    Return cached `rates` dict if timestamp is < 24 h old.
    """
    result = await db.execute(
        select(ExchangeRateCache).where(
            ExchangeRateCache.base_currency == base_currency
        )
    )
    entry = result.scalar_one_or_none()

    if entry and (datetime.now(timezone.utc) - entry.timestamp) < CACHE_DURATION:
        return entry.rates
    return None


async def update_cache(
    db: AsyncSession, base_currency: str, rates: dict
) -> dict:
    """
    Insert or update exchange-rate cache row, then commit.
    """
    utc_now = datetime.now(timezone.utc)

    result = await db.execute(
        select(ExchangeRateCache).where(
            ExchangeRateCache.base_currency == base_currency
        )
    )
    entry = result.scalar_one_or_none()

    if entry:
        entry.rates = rates
        entry.timestamp = utc_now
    else:
        entry = ExchangeRateCache(
            base_currency=base_currency,
            rates=rates,
            timestamp=utc_now,
        )
        db.add(entry)

    await db.commit()
    return rates
