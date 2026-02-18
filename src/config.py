import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env.dev", env_file_encoding="utf-8", case_sensitive=True
    )
    PROJECT_NAME: str
    API_VERSION: str
    ENV: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str

    SERVER_HOST: str
    SERVER_PORT: int

class ContainerDevSettings(Settings):
    model_config = SettingsConfigDict(
        env_file="./.env.dev", env_file_encoding="utf-8", case_sensitive=True
    )
    ENV: str = "dev"

class ContainerTestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file="./.env.test", env_file_encoding="utf-8", case_sensitive=True
    )
    ENV: str = "test"

def get_settings(env: str = "dev") -> Settings:
    """
    Return the settings object based on the environment.

    Parameters:
        env (str): The environment to retrieve the settings for. Defaults to "dev".

    Returns:
        Settings: The settings object based on the environment.

    Raises:
        ValueError: If the environment is invalid.
    """
    if env.lower() in ["dev", "d", "development"]:
        return ContainerDevSettings()
    if env.lower() in ["test", "t", "testing"]:
        return ContainerTestSettings()

    raise ValueError("Invalid environment. Must be 'dev' or 'test'")

_env = os.environ.get("ENV", "dev")

settings = get_settings(env=_env)
