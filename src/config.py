from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env.dev"), env_file_encoding="utf-8", case_sensitive=True
    )

    PROJECT_NAME: str
    API_VERSION: str
    ENV: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    SERVER_HOST: str
    SERVER_PORT: int


class ContainerDevSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env.dev"), env_file_encoding="utf-8", case_sensitive=True
    )


class ContainerTestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env.test"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


def get_settings(env: str = "dev") -> Settings:
    """
    Get settings object with .env values of a particular environment.

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


dev_settings = get_settings("dev")
test_settings = get_settings("test")
