from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.expense_schema import ExpenseIn, ExpenseOut
from app.repositories.expense_repository import *
from app.db.session import get_db
from app.models.expense import Expense

router = APIRouter()

@router.post("/", response_model=ExpenseOut)
async def create(expense_data: ExpenseIn, db: AsyncSession = Depends(get_db)):
    expense = Expense(**expense_data.dict())
    return await create_expense(db, expense)

@router.get("/", response_model=list[ExpenseOut])
async def list_all(
    db: AsyncSession = Depends(get_db),
    trip_id: int = Query(default=None),
    date: str = Query(default=None)
):
    return await list_expenses(db, trip_id, date)

@router.delete("/{expense_id}")
async def delete(expense_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_expense(db, expense_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"status": "deleted"}
