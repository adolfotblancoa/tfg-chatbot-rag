from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TFG CHATBOT RAG"
    debug: bool = True
    sqlite_db_path: str = "./app.db"
    openai_api_key: str = ""
    chroma_db_path: str = "./chroma_db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()