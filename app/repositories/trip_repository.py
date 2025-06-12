from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.trip import Trip

async def create_trip(session: AsyncSession, trip: Trip) -> Trip:
    session.add(trip)
    await session.commit()
    await session.refresh(trip)
    return trip

async def list_trips(session: AsyncSession) -> list[Trip]:
    result = await session.execute(select(Trip))
    return result.scalars().all()

async def delete_trip(session: AsyncSession, trip_id: int) -> bool:
    trip = await session.get(Trip, trip_id)
    if not trip:
        return False
    await session.delete(trip)
    await session.commit()
    return True
