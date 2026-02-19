import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.database import get_db, TEST_DATABASE_URL


@pytest.fixture
async def client():
    """AsyncClient generator fixture for running tests"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


def get_test_local_session() -> async_sessionmaker:
    """
    Database session factory -- creates and returns an async_sessionmaker
    object for a database session.

    Returns:
        An async_sessionmaker object configured for the test database session.
    """
    session_factory = async_sessionmaker(bind=engine, autoflush=False)
    return session_factory


async def get_test_db() -> AsyncGenerator[AsyncSession]:
    """
    Returns a generator that yields a session for test database

    Yields:
        Session: A session object for test database
    """
    db = get_test_local_session()
    async with db() as session:
        yield session


# AsyncEngine attached to the testing database
engine = create_async_engine(TEST_DATABASE_URL, echo=False)

app.dependency_overrides[get_db] = get_test_db
