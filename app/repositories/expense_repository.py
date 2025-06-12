from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.expense import Expense
from sqlalchemy import and_
from sqlalchemy import String

async def create_expense(session: AsyncSession, expense: Expense) -> Expense:
    session.add(expense)
    await session.commit()
    await session.refresh(expense)
    return expense

async def list_expenses(session: AsyncSession, trip_id: int = None, date: str = None) -> list[Expense]:
    query = select(Expense)
    if trip_id:
        query = query.where(Expense.trip_id == trip_id)
    if date:
        query = query.where(Expense.created_at.cast(String).like(f"{date}%"))
    result = await session.execute(query)
    return result.scalars().all()

async def delete_expense(session: AsyncSession, expense_id: int) -> bool:
    expense = await session.get(Expense, expense_id)
    if not expense:
        return False
    await session.delete(expense)
    await session.commit()
    return True
