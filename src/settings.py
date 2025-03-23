import os
from typing import Optional
from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    OPENHANDS_URL: AnyHttpUrl = "http://localhost:51090"
    OPENHANDS_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_prefix = "SWARM_DIRECTIVE_"

settings = Settings()