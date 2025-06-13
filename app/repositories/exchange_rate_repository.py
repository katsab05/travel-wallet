"""
Exchange rate Repository

Provides direct database access functions for Echange Rate model.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from app.models.exhange_rate_cache import ExchangeRateCache

CACHE_DURATION = timedelta(hours=24)

async def get_cached_rates(db: AsyncSession, base_currency: str):
    """
    Fetch cached rates if they're fresh (<24h).
    """
    result = await db.execute(
        select(ExchangeRateCache).where(ExchangeRateCache.base_currency == base_currency)
    )
    entry = result.scalar_one_or_none()

    if entry and (datetime.utcnow() - entry.timestamp) < CACHE_DURATION:
        return entry.rates
    return None

async def update_cache(db: AsyncSession, base_currency: str, rates: dict):
    """
    Update or insert new cache into DB.
    """
    result = await db.execute(
        select(ExchangeRateCache).where(ExchangeRateCache.base_currency == base_currency)
    )
    entry = result.scalar_one_or_none()

    if entry:
        entry.rates = rates
        entry.timestamp = datetime.utcnow()
    else:
        entry = ExchangeRateCache(
            base_currency=base_currency,
            rates=rates,
            timestamp=datetime.utcnow()
        )
        db.add(entry)

    await db.commit()
    return entry.rates
