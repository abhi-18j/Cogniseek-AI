from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "omnis-backend"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database settings (default values match docker-compose)
    DATABASE_HOST: str = Field("postgres")
    DATABASE_PORT: int = Field(5432)
    DATABASE_USER: str = Field("omni")
    DATABASE_PASSWORD: str = Field("omni_password")
    DATABASE_NAME: str = Field("omnis")

    # Pydantic v2 / pydantic-settings configuration
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    # )
    model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
)

    @property
    def DATABASE_URL(self) -> str:
        """Return SQLAlchemy async URL using asyncpg driver."""
        user = self.DATABASE_USER
        pw = self.DATABASE_PASSWORD
        host = self.DATABASE_HOST
        port = self.DATABASE_PORT
        name = self.DATABASE_NAME
        return f"postgresql+asyncpg://{user}:{pw}@{host}:{port}/{name}"


settings = Settings()
