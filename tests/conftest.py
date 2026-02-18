from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.database import SQLALCHEMY_DATABASE_URL


@pytest.fixture
async def client():
    """AsyncClient generator fixture for running tests"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


# _test_settings = get_settings("test")
# TEST_SQLALCHEMY_DATABASE_URL = (
#     f"""postgresql+asyncpg://{_test_settings.POSTGRES_USER}:
#     {_test_settings.POSTGRES_PASSWORD}@{_test_settings.POSTGRES_HOST}
#     :{_test_settings.POSTGRES_PORT}/{_test_settings.POSTGRES_DB}"""
# )

# AsyncEngine attached to the testing database
# engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=False)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)


@pytest.fixture
def get_test_local_session() -> async_sessionmaker:
    """
    Database session factory -- creates and returns an async_sessionmaker
    object for a database session.

    Returns:
        An async_sessionmaker object configured for the test database session.
    """
    session_factory = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return session_factory


@pytest.fixture
async def get_test_db(get_test_local_session) -> AsyncGenerator:
    """
    Returns a generator that yields a session for test database

    Yields:
        Session: A session object for test database
    """
    db = get_test_local_session()
    async with db as session:
        yield session
