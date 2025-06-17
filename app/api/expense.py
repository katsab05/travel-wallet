"""
Expense API

Endpoints for creating,getting all, and deleting expense.
All routes require a valid JWT (get_current_user).
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from core.deps import get_current_user
from app.schemas.expense_schema import ExpenseIn, ExpenseOut
from app.services import expense_service

router = APIRouter()


@router.post(
    "/", 
    response_model=ExpenseOut, 
    status_code=status.HTTP_201_CREATED   # ✅ tests expect 201
)
async def create_expense(
    expense_data: ExpenseIn,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Create a new expense linked to a trip.
    """
    expense = await expense_service.create_expense_service(db, expense_data, user_id=user.id)
    return expense                       


@router.get("/", response_model=list[ExpenseOut])
async def get_all_expenses(
    trip_id: int | None = Query(default=None),
    date: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Retrieve expenses for a given trip and/or date.
    """
    return await expense_service.get_expense_service(db=db, trip_id=trip_id, date=date, user_id=user.id)


@router.delete("/{expense_id}", status_code=status.HTTP_200_OK)
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Delete an expense by its ID.
    """
    success = await expense_service.delete_expense_service(db, expense_id, user_id=user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"status": "deleted"}
