from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file="settings.toml")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_FILE: str = "fleetpulse.db"
    PROJECT_NAME: str = "FleetPulse"
    SECRET_KEY: str = "change-me"


settings = Settings()