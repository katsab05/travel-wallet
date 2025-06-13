"""
Expense Service

Provides business logic for creating, fetching, and deleting expenses.
Interacts with the repository layer and handles data transformation.
"""

from app.models.expense import Expense
from app.schemas.expense_schema import ExpenseIn
from app.repositories import expense_repository
from sqlalchemy.ext.asyncio import AsyncSession


async def create_expense_service(db: AsyncSession, expense_data: ExpenseIn) -> Expense:
    """
    Creates a new expense record.

    - Converts incoming Pydantic model into ORM model
    - Delegates creation to the repository layer

    Args:
        db (AsyncSession): Active DB session
        expense_data (ExpenseIn): Validated user input

    Returns:
        Expense: Newly created expense model instance
    """
    # Convert the validated schema to a database model
    expense = Expense(**expense_data.dict())

    # Call repository function to insert into DB
    return await expense_repository.create(db, expense)


async def get_expense_service(
    db: AsyncSession,
    trip_id: int | None = None,
    date: str | None = None
) -> list[Expense]:
    """
    Retrieve expenses by trip id.

    Args:
        db (AsyncSession): Active DB session
        trip_id (int): Filter by trip ID

    Returns:
        list[Expense]: List of matching expenses
    """
    return await expense_repository.get_by_trip_id(db, trip_id, date)


async def delete_expense_service(db: AsyncSession, expense_id: int) -> bool:
    """
    Delete an expense by ID.

    Args:
        db (AsyncSession): Active DB session
        expense_id (int): ID of the expense to delete

    Returns:
        bool: True if deleted successfully, False otherwise
    """
    # Return True if delete was successful
    return await expense_repository.delete_by_trip_id(db, expense_id)
