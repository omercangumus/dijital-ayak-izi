import os
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from pathlib import Path

# .env dosyasini backend/ altinda ara
env_path = Path(__file__).parent.parent.parent / "config.env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseModel):
    env: str = os.getenv("ENV", "dev")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-prod")
    access_token_exp_minutes: int = int(os.getenv("ACCESS_TOKEN_EXP_MIN", "60"))
    email_verify_exp_hours: int = int(os.getenv("EMAIL_VERIFY_EXP_H", "24"))
    sqlite_url: str = os.getenv("SQLITE_URL", "sqlite:///./data.db")
    cors_origins: list[str] = [o for o in os.getenv("CORS_ORIGINS", "*").split(",") if o]
    offline_mode: bool = os.getenv("OFFLINE_MODE", "false").lower() in ("1", "true", "yes")
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    google_search_engine_id: str | None = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    scraperapi_key: str | None = os.getenv("SCRAPERAPI_KEY")
    hibp_api_key: str | None = os.getenv("HIBP_API_KEY")
    synthetic_mode: bool = os.getenv("SYNTHETIC_MODE", "false").lower() in ("1", "true", "yes")
    
    # Yeni Google API'leri
    google_maps_api_key: str | None = os.getenv("GOOGLE_MAPS_API_KEY")
    google_places_api_key: str | None = os.getenv("GOOGLE_PLACES_API_KEY")
    google_youtube_api_key: str | None = os.getenv("GOOGLE_YOUTUBE_API_KEY")
    google_vision_api_key: str | None = os.getenv("GOOGLE_VISION_API_KEY")


settings = Settings()

# Debug: Print settings at startup
print("=" * 50)
print("CONFIG LOADED:")
print(f"  ENV: {settings.env}")
print(f"  GOOGLE_API_KEY: {'[OK]' if settings.google_api_key else '[NO]'}")
print(f"  GOOGLE_SEARCH_ENGINE_ID: {'[OK]' if settings.google_search_engine_id else '[NO]'}")
print(f"  GOOGLE_MAPS_API_KEY: {'[OK]' if settings.google_maps_api_key else '[NO]'}")
print(f"  GOOGLE_PLACES_API_KEY: {'[OK]' if settings.google_places_api_key else '[NO]'}")
print(f"  GOOGLE_YOUTUBE_API_KEY: {'[OK]' if settings.google_youtube_api_key else '[NO]'}")
print(f"  GOOGLE_VISION_API_KEY: {'[OK]' if settings.google_vision_api_key else '[NO]'}")
print(f"  SCRAPERAPI_KEY: {'[OK]' if settings.scraperapi_key else '[NO]'}")
print(f"  HIBP_API_KEY: {'[OK]' if settings.hibp_api_key else '[NO]'}")
print(f"  SYNTHETIC_MODE: {settings.synthetic_mode}")
print(f"  OFFLINE_MODE: {settings.offline_mode}")
print("=" * 50)
