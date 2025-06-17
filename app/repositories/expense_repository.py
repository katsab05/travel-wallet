"""
Expense Repository

Provides direct database access functions for Expense model.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from app.models.expense import Expense


async def create(db: AsyncSession, expense: Expense) -> Expense:
    """
    Insert a new expense record into the database.

    Args:
        db (AsyncSession): Active DB session
        expense (Expense): Expense instance to add

    Returns:
        Expense: The newly persisted record
    """
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


async def get_by_trip_id(
        db: AsyncSession, 
        trip_id: int,
        date: str | None = None,
        user_id: int = None
                         ) -> list[Expense]:
    """
    Fetch all expenses associated with a given trip ID.

    Args:
        db (AsyncSession): Active DB session
        trip_id (int): Trip foreign key

    Returns:
        list[Expense]: List of matching expenses
    """
    query = select(Expense).where(Expense.user_id == user_id)

    if trip_id is not None:
        query = query.where(Expense.trip_id == trip_id)

    if date is not None:
        query = query.where(func.date(Expense.timestamp) == date)

    result = await db.execute(query)
    return result.scalars().all()

async def delete_by_trip_id(db: AsyncSession, expense_id: int) -> None:
    """
    Delete an expense from the database by its ID.

    Args:
        db (AsyncSession): Active DB session
        expense_id (int): ID of the expense to delete

    Returns:
        None
    """
    await db.execute(delete(Expense).where(Expense.id == expense_id))
    await db.commit()
