from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    HUSK_NAME: str = "Husk"
    HUSK_ENV: str = "development"

    LLM_API_KEY: str
    LLM_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    DEFAULT_MODEL: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings globally
settings = Settings()