import os
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from seed_data import seed_initial_data
from .config import settings
from .init_db import create_tables
from .routes.auth import router as auth_router
from .routes.bookings import router as bookings_router
from .routes.movies import router as movies_router
from .routes.theaters import router as theaters_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("SKIP_DB_INIT") == "1":
        yield
        return
    if settings.auto_create_tables:
        create_tables()
        seed_initial_data()
    yield


is_prod = settings.environment == "production"

app = FastAPI(
    title="Movie Booking System API",
    lifespan=lifespan,
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
    openapi_url=None if is_prod else "/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

api_prefix = "/api/v1"

app.include_router(auth_router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(movies_router, prefix=f"{api_prefix}/movies", tags=["Movies"])
app.include_router(bookings_router, prefix=f"{api_prefix}/bookings", tags=["Bookings"])
app.include_router(theaters_router, prefix=f"{api_prefix}/theaters", tags=["Theaters"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Booking System API"}


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled server error")
    if settings.debug:
        raise exc
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
