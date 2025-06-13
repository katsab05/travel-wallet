"""
Exchange rate Cache Service.

Encapsulates logic for caching exchange rates.
"""

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.exchange_rate_repository import get_cached_rates, update_cache

API_URL = "https://api.exchangerate-api.com/v4/latest/"

async def fetch_exchange_rates(base_currency: str, db: AsyncSession) -> dict:
    """
    Return exchange rates either from DB (if fresh) or external API.
    """
    cached = await get_cached_rates(db, base_currency)
    if cached:
        return cached

    # Fetch from external API
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}{base_currency}")
        if response.status_code != 200:
            raise Exception("Failed to fetch exchange rates")

        data = response.json()
        rates = data["rates"]

        # Save to DB
        return await update_cache(db, base_currency, rates)

async def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str = "USD",
    db: AsyncSession = None
) -> float:
    """
    Converts an amount from one currency to another using cached or live rates.
    """
    rates = await fetch_exchange_rates(from_currency, db)
    rate = rates.get(to_currency)
    if rate is None:
        raise ValueError(f"Currency {to_currency} not found.")
    return amount * rate
