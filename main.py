from fastapi import FastAPI
from app.api import trip, expense

app = FastAPI()

app.include_router(trip.router, prefix="/trips", tags=["Trips"])
app.include_router(expense.router, prefix="/expenses", tags=["Expenses"])
