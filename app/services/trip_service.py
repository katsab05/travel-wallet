"""
Trip Service

Handles business logic related to Trip model.
Used by the API layer to delegate Trip creation, retrieval, and deletion.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trip import Trip
from app.schemas.trip_schema import TripIn
from app.repositories import trip_repository


async def create_trip_service(db: AsyncSession, trip_data: TripIn, user_id: int) -> Trip:
    """
    Create a new trip from validated schema data.

    Args:
        db (AsyncSession): Active DB session
        trip_data (TripIn): Validated input data from the client

    Returns:
        Trip: Newly created trip instance
    """
    trip = Trip(**trip_data.dict(),
                user_id =user_id)
    return await trip_repository.create(db, trip)


async def get_all_trips_service(db: AsyncSession, user_id:int) -> list[Trip]:
    """
    Retrieve all trips from the database.

    Args:
        db (AsyncSession): Active DB session

    Returns:
        list[Trip]: All trips stored in the system
    """
    return await trip_repository.get_all_trips(db)


async def delete_trip_service(db: AsyncSession, trip_id: int) -> bool:
    """
    Delete a trip by its ID.

    Args:
        db (AsyncSession): Active DB session
        trip_id (int): ID of the trip to delete

    Returns:
        bool: True if deleted successfully, False otherwise
    """
    return await trip_repository.delete_trip_by_id(db, trip_id)
