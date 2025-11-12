from pydantic import AnyUrl
from pydantic_settings import BaseSettings
import os
class Settings(BaseSettings):
    # Core
    ENV: str = "dev"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me"
    DATABASE_URL: AnyUrl | str = "sqlite+aiosqlite:///./data.db"

    # External API keys / endpoints
    GOOGLE_SAFE_BROWSING_API_KEY: str | None = None
    VIRUSTOTAL_API_KEY: str | None = None
    SSLLABS_API_URL: str = "https://api.ssllabs.com/api/v3/"
    PHISHTANK_API_KEY: str | None = None  # optional if using public feed
    PHISHTANK_API_URL: str = "https://phishtank.org/"

    # Risk scoring weights (tweakable)
    WEIGHT_GSB: float = 0.45
    WEIGHT_VT: float = 0.35
    WEIGHT_SSL: float = 0.10
    WEIGHT_PHISH: float = 0.10

    class Config:
        env_file = ".env"

settings = Settings()
