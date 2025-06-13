"""
Expense API

Handles creation, listing, and deletion of user expenses.
Uses service layer for business logic.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from core.deps import get_current_user
from app.schemas.expense_schema import ExpenseIn, ExpenseOut
from app.services import expense_service

router = APIRouter()


@router.post("/", response_model=ExpenseOut)
async def create_expense(
    expense_data: ExpenseIn,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Create a new expense linked to a trip.

    Args:
        expense_data (ExpenseIn): Input expense data
        db (AsyncSession): DB session
        user (User): Authenticated user (via JWT)

    Returns:
        ExpenseOut: Created expense
    """
    return await expense_service.create_expense_service(db, expense_data)


@router.get("/", response_model=list[ExpenseOut])
async def get_all_expenses(
    trip_id: int = Query(default=None),
    date: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Retrieve expenses for a given trip and/or date.

    Args:
        trip_id (int): Trip ID to filter
        date (str): Date filter (optional)
        db (AsyncSession): DB session
        user (User): Authenticated user

    Returns:
        list[ExpenseOut]: Filtered list of expenses
    """
    return await expense_service.get_expense_service(db, trip_id, date)


@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Delete an expense by its ID.

    Args:
        expense_id (int): ID of the expense
        db (AsyncSession): DB session
        user (User): Authenticated user

    Returns:
        dict: Deletion status
    """
    success = await expense_service.delete_expense_service(db, expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"status": "deleted"}
