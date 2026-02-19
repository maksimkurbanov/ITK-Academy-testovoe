import pytest
from src.api.v1.wallets.models import Base
from tests.conftest import engine


@pytest.fixture(scope="function", autouse=True)
async def setup_and_teardown():
    """
    Janitor fixture that sets up and tears down test database
    tables based on SQLAlchemy models, so each test maintains
    maximum test-isolation. Applied to all tests
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
