from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = Field(default="rag-document-assistant")
    app_env: str = Field(default="local")
    log_level: str = Field(default="info")
    llm_provider: str = Field(default="mock")
    openai_api_key: str | None = None
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()