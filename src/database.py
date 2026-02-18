from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from src.config import Settings, settings
from typing import AsyncGenerator


def build_sqlalchemy_database_url_from_settings(_settings: Settings) -> str:
    """
    Builds a SQLAlchemy URL based on the provided settings.

    Parameters:
        _settings (Settings): An instance of the Settings class
        containing the PostgreSQL connection details.

    Returns:
        str: The generated SQLAlchemy URL.
    """
    return (
        f"postgresql+asyncpg://{_settings.POSTGRES_USER}:{_settings.POSTGRES_PASSWORD}"
        f"@{_settings.POSTGRES_HOST}:{_settings.POSTGRES_PORT}/{_settings.POSTGRES_DB}"
    )

def get_engine(database_url: str, echo=False) -> AsyncEngine:
    """
    Creates and returns a SQLAlchemy Engine object for connecting to a database.

    Parameters:
        database_url (str): The URL of the database to connect to.
        Defaults to SQLALCHEMY_DATABASE_URL.
        echo (bool): Whether or not to enable echoing of SQL statements.
        Defaults to False.

    Returns:
        Engine: A SQLAlchemy Engine object representing the database connection.
    """
    engine = create_async_engine(database_url, echo=echo)
    return engine

def get_local_session(database_url: str, echo=False, **kwargs) -> async_sessionmaker:
    """
    Create and return a sessionmaker object for a local database session.

    Parameters:
        database_url (str): The URL of the local database.
        Defaults to `SQLALCHEMY_DATABASE_URL`.
        echo (bool): Whether to echo SQL statements to the console.
        Defaults to `False`.

    Returns:
        sessionmaker: A sessionmaker object configured for the local database session.
    """
    engine = get_engine(database_url, echo)
    session = async_sessionmaker(bind=engine, autoflush=False)
    return session

async def get_session() -> AsyncGenerator:
    """
    Returns a generator that yields a database session

    Yields:
        Session: A database session object.
    """

    db = get_local_session(SQLALCHEMY_DATABASE_URL, False)()
    async with db as session:
        yield session

@contextmanager
async def get_ctx_db(database_url: str) -> AsyncGenerator:
    """
    Context manager that creates a database session and yields
    it for use in a 'with' statement.

    Parameters:
        database_url (str): The URL of the database to connect to.

    Yields:
        Generator: A database session.

    Raises:
        Exception: If an error occurs while getting the database session.

    """
    db = get_local_session(database_url)()
    async with db as session:
        yield session


# async def get_session():
#     async with get_local_session(SQLALCHEMY_DATABASE_URL) as session:
#         yield session

load_dotenv()
SQLALCHEMY_DATABASE_URL = build_sqlalchemy_database_url_from_settings(settings)




# engine = create_async_engine(config.DB_URL, echo=True)
# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
#     autoflush=False,
# )
#
# async def get_session():
#     async with AsyncSessionLocal() as session:
#          yield session
