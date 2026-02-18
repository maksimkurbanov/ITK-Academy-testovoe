import pytest
from src.api.v1.wallets.models import Base
from tests.conftest import engine
# from tests.conftest import TEST_SQLALCHEMY_DATABASE_URL
from scripts.initdb import seed_database
from src.config import get_settings
from tests.conftest import engine



@pytest.fixture(scope="function", autouse=True)
async def setup_and_teardown(get_test_db):
    """Async fixture that recreates tables before and after each test."""
    async with get_test_db as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all(bind=engine))
        except Exception:
            pass
        await conn.run_sync(Base.metadata.create_all(bind=engine))
    # yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    yield
    await get_test_db.run_sync(Base.metadata.drop_all(bind=engine))

@pytest.fixture
def seed_test_database():
    seed_database("test")


@pytest.fixture
def test_settings():
    return get_settings("test")

@pytest.fixture
async def get_test_db(get_test_local_session):
    db = get_test_local_session()
    async with db as session:
        yield session
