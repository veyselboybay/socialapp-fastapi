from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_connection: str 
    secret: str 

    model_config = SettingsConfigDict(env_file='./app/.env')

settings = Settings()