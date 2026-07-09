import logging
from src.logger import setup_logging
from fastapi import FastAPI 
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import reviews_router
from contextlib import asynccontextmanager
from src.db.main import init_db

setup_logging()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def life_span(app: FastAPI):
    logger.info("server is starting ...")
    await init_db()
    yield 
    logger.info("server has been stopped")

version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(reviews_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
