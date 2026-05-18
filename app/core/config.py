from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TFG CHATBOT RAG"
    debug: bool = True
    sqlite_db_path: str = "./app.db"
    openai_api_key: str = ""
    chroma_db_path: str = "./chroma_db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    whatsapp_verify_token: str = ""
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_api_version: str = "v20.0"


settings = Settings()