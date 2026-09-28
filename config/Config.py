from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # SQL
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
#Variável que armazena os valores lidos do arquivo .env
settings = Settings()