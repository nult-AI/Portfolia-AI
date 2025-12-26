from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Any, Dict
from pydantic import field_validator, model_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Portfolio API"
    API_V1_STR: str = "/api/v1"
    
    # Database individual components
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    # Computed or direct URL
    DATABASE_URL: Optional[str] = None

    @model_validator(mode='after')
    def assemble_db_connection(self) -> 'Settings':
        if self.DATABASE_URL:
            return self
        
        # Build URL from components if not provided
        url = f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
        # Add sslmode=require for remote Supabase
        if self.DB_HOST not in ["127.0.0.1", "localhost"]:
            url += "?sslmode=require"
            
        self.DATABASE_URL = url
        return self

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
