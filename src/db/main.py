from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from src.config import Config
from src.books.models import Book
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    Config.database_url,
    echo=True,
    connect_args={
        "ssl": True
    }
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    Session = sessionmaker(
        bind=engine,
        class_= AsyncSession,
        expire_on_commit = False
    )

    async with Session() as session:
        yield session