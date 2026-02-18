import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from src.api.v1.wallets.models import Base
from src.database import SQLALCHEMY_DATABASE_URL


@pytest.fixture(scope="function", autouse=True)
async def setup_and_teardown():
    """
    Janitor fixture that sets up and tears down test database
    tables based on SQLAlchemy models, so each test maintains
    maximum test-isolation. Applied to all tests
    """
    # janitor_engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL)
    janitor_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    async with janitor_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with janitor_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await janitor_engine.dispose()
