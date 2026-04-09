from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    debug: bool = False
    django_secret_key: str
    ollama_host: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()