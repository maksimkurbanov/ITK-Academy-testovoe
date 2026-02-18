from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine, async_session
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.config import get_settings
from src.config import settings as _tsettings
from src.database import get_session
from dotenv import load_dotenv
import os


load_dotenv("../.env.test")
print("DB var in conftest.py after load_dotenv: ", os.getenv("POSTGRES_HOST"))

def test_settings():
    return get_settings("test")

_test_settings = get_settings("test")
print("DB var in conftest.py from _test_settings: ", os.getenv("POSTGRES_HOST"))
print("Test_settings_dict: ", _test_settings.__dict__)


# TEST_SQLALCHEMY_DATABASE_URL = (
#     f"postgresql+asyncpg://{_test_settings.POSTGRES_USER}:{_test_settings.POSTGRES_PASSWORD}@"
#     f"{_test_settings.POSTGRES_HOST}:{_test_settings.POSTGRES_PORT}/{_test_settings.POSTGRES_DB}"
# )
#
# @pytest.fixture
# def test_sqlalchemy_database_url():
#     return TEST_SQLALCHEMY_DATABASE_URL
#
#
# def get_test_engine(database_url: str, echo=False) -> AsyncEngine:
#     _engine = create_async_engine(database_url, echo=echo)
#     return _engine
#
# # @pytest.fixture()
# # async def client():
# #     async with AsyncClient() as client:
# #         yield client
#
# @pytest.fixture
# def get_test_local_session(database_url: str, echo=False) -> async_sessionmaker:
#     _engine = get_test_engine(database_url, echo=echo)
#     session_factory = async_sessionmaker(bind=_engine, autoflush=False, autocommit=False)
#     return session_factory
#
# # async def get_test_local_session(database_url: str, echo=False, **kwargs) -> async_sessionmaker:
# #
# #     session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)
# #     return session
#
#
# async def override_get_session() -> AsyncGenerator:
#     db = get_test_local_session(TEST_SQLALCHEMY_DATABASE_URL, echo=False)()
#     async with db as session:
#         yield session
#
# @pytest.fixture
# async def client():
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
#         yield client
#
#
#
# app.dependency_overrides[get_session] = override_get_session
# engine = get_test_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=False)
#################################

TEST_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{_test_settings.POSTGRES_USER}:{_test_settings.POSTGRES_PASSWORD}@"
    f"{_test_settings.POSTGRES_HOST}:{_test_settings.POSTGRES_PORT}/{_test_settings.POSTGRES_DB}"
)

@pytest.fixture
def test_sqlalchemy_database_url():
    return TEST_SQLALCHEMY_DATABASE_URL

@pytest.fixture
def get_test_engine(test_sqlalchemy_database_url, echo=False) -> AsyncEngine:
    _engine = create_async_engine(test_sqlalchemy_database_url, echo=echo)
    return _engine

# @pytest.fixture()
# async def client():
#     async with AsyncClient() as client:
#         yield client

@pytest.fixture
def get_test_local_session(get_test_engine, echo=False) -> async_sessionmaker:
    session_factory = async_sessionmaker(bind=get_test_engine, autoflush=False, autocommit=False)
    return session_factory

# async def get_test_local_session(database_url: str, echo=False, **kwargs) -> async_sessionmaker:
#
#     session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)
#     return session


async def override_get_session() -> AsyncGenerator:
    db = get_test_local_session(TEST_SQLALCHEMY_DATABASE_URL, echo=False)()
    async with db as session:
        yield session

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client



app.dependency_overrides[get_session] = override_get_session
engine = get_test_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=False)
# engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=False)


# INITIAL from the internet:
#
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
#
# from settings import get_settings
#
#
# @pytest.fixture()
# async def get_engine():
#     engine = create_async_engine(get_settings().test_db_url)
#     yield engine
#     await engine.dispose()
#
#
# @pytest.fixture()
# async def db_session(get_engine) -> AsyncSession:
#     async with get_engine.begin() as connection:
#         async with async_session(bind=connection) as session:
#             yield session
#             await session.close()
#
#
# @pytest.fixture()
# def override_get_async_session(db_session: AsyncSession) -> Callable:
#     async def _override_get_async_session():
#         yield db_session
#
#     return _override_get_async_session

# With my edits
#
# @pytest.fixture()
# async def get_engine():
#     engine = create_async_engine(test_sqlalchemy_database_url())
#     yield engine
#     await engine.dispose()
#
# @pytest.fixture()
# async def db_session(get_engine) -> AsyncSession:
#     async with get_engine.begin() as connection:
#         async with async_session(bind=connection) as session:
#             yield session
#             await session.close()
#
#
# @pytest.fixture()
# def override_get_async_session(db_session: AsyncSession) -> Callable:
#     async def _override_get_async_session():
#         yield db_session
#
#     return _override_get_async_session

##########
# DeepSeek's version:

# import pytest
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from app.main import app
# from app.database import get_db, Base
#
# TEST_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/test_db"
# async_engine = create_async_engine(TEST_DATABASE_URL)
# AsyncTestingSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
#
# @pytest.fixture(scope="session")
# async def create_test_database():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
# @pytest.fixture
# async def db_session(create_test_database):
#     async with async_engine.connect() as connection:
#         async with connection.begin() as transaction:
#             async with AsyncTestingSessionLocal(bind=connection) as session:
#                 # Nested transaction for isolation
#                 await session.begin_nested()
#                 yield session
#                 await transaction.rollback()
#
# @pytest.fixture
# async def client(db_session):
#     async def override_get_db():
#         yield db_session
#
#     app.dependency_overrides[get_db] = override_get_db
#     async with AsyncClient(app=app, base_url="http://test") as test_client:
#         yield test_client
#     app.dependency_overrides.clear()

# import pytest
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from src.api.v1.wallets.models import Base
#
#
#
# TEST_DATABASE_URL = "postgresql+asyncpg://test:test@test-db/itk-pg"
# async_engine = create_async_engine(TEST_DATABASE_URL)
# AsyncTestingSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
#
# @pytest.fixture
# async def create_test_database():
#     async with async_engine.begin() as conn:
#         try:
#             await conn.run_sync(Base.metadata.drop_all)
#         except Exception as e:
#             pass
#         await conn.run_sync(Base.metadata.create_all)
#         yield
#     # async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
# @pytest.fixture
# async def db_session(create_test_database):
#     async with async_engine.connect() as connection:
#         async with connection.begin() as transaction:
#             async with AsyncTestingSessionLocal(bind=connection) as session:
#                 # Nested transaction for isolation
#                 await session.begin_nested()
#                 yield session
#                 await transaction.rollback()
#
# @pytest.fixture
# async def client(db_session):
#     async def override_get_db():
#         print("POSTGRES_USER VAR: ", os.getenv("POSTGRES_USER"))
#         yield db_session
#
#     app.dependency_overrides[get_session] = override_get_db
#     print("DEPENDENCY OVERRIDE is CALLED")
#     print("POSTGRES_USER VAR: ", os.getenv("POSTGRES_USER"))
#     # async with AsyncClient(app=app, base_url="http://test") as test_client:
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
#         yield test_client
#     # app.dependency_overrides.clear()