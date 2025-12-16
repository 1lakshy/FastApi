from fastapi import APIRouter, Header, status,FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Starting server...")
    await init_db()
    yield
    print(f"Shutting down server...")

version = "v1"

app = FastAPI(
    title = "Book Management API",
    description = "An API to manage a collection of books.",
    version = version,
    lifespan=life_span

)

app.include_router(book_router,prefix=f"/api/{version}/books")