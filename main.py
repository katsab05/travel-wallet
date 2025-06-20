from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from core.logger import logger
from fastapi import FastAPI


from fastapi import FastAPI
from app.api import trip, expense, auth, document, attraction

app = FastAPI()

# routes
app.include_router(trip.router, prefix="/trips", tags=["trips"])
app.include_router(expense.router, prefix="/expenses", tags=["expenses"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(document.router, prefix='/documents', tags=["documents)"])
app.include_router(attraction.router, prefix='/attractions', tags=["attractions"])

# errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {repr(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )