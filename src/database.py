from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

from src.config import dev_settings, test_settings, Settings
from typing import AsyncGenerator


def build_sqlalchemy_database_url_from_settings(settings: Settings) -> str:
    """
    Builds a SQLAlchemy database URL based on the provided settings.

    Parameters:
        settings (Settings): An instance of Settings object
        containing PostgreSQL connection details.

    Returns:
        str: Generated SQLAlchemy database URL.
    """
    return (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
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


def get_local_session(database_url: str, echo=False) -> async_sessionmaker:
    """
    Database session factory -- create and return an async_sessionmaker
    object for a database session.

    Parameters:
        database_url (str): The URL of the local database.
        Defaults to `SQLALCHEMY_DATABASE_URL`.
        echo (bool): Whether to echo SQL statements to the console.
        Defaults to `False`.

    Returns:
        async_sessionmaker: An async_sessionmaker object configured
        for the DEV database session.
    """
    engine = get_engine(database_url, echo)
    session = async_sessionmaker(bind=engine, autoflush=False)
    return session


async def get_db() -> AsyncGenerator[AsyncSession]:
    """
    Returns a generator that yields a database session for path-operations
    requiring database access

    Yields:
        Session: A database session object.
    """

    db = get_local_session(DEV_DATABASE_URL, False)()
    async with db as session:
        yield session


DEV_DATABASE_URL = build_sqlalchemy_database_url_from_settings(dev_settings)
TEST_DATABASE_URL = build_sqlalchemy_database_url_from_settings(test_settings)
