from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_connection: str 
    secret: str 
    algorithm: str
    expires_in: int

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
