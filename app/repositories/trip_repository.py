"""
Trip Repository Layer.

Handles all database interactions related to trips.
"""


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.trip import Trip

async def create_trip(session: AsyncSession, trip: Trip) -> Trip:
    """
    Add a new trip record to the database.

    Args:
        db (AsyncSession): Database session.
        trip_data (TripIn): Input data for new trip.

    Returns:
        Trip: Created trip object.
    """
    session.add(trip)
    await session.commit()
    await session.refresh(trip)
    return trip

async def list_trips(session: AsyncSession) -> list[Trip]:
    """
    Retrieve all trips from the database.

    Args:
        db (AsyncSession): SQLAlchemy async session.

    Returns:
        list[Trip]: List of all trip records.
    """
    result = await session.execute(select(Trip))
    return result.scalars().all()

async def delete_trip(session: AsyncSession, trip_id: int) -> bool:
    """
    Delete a trip by trip ID.

    Args:
        db (AsyncSession): Database session.
        trip_id (int): Trip ID to delete.
    """
    trip = await session.get(Trip, trip_id)
    if not trip:
        return False
    await session.delete(trip)
    await session.commit()
    return True
