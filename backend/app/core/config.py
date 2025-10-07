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
    serpapi_key: str | None = os.getenv("SERPAPI_KEY")
    hibp_api_key: str | None = os.getenv("HIBP_API_KEY")
    synthetic_mode: bool = os.getenv("SYNTHETIC_MODE", "false").lower() in ("1", "true", "yes")


settings = Settings()

# Debug: Print settings at startup
print("=" * 50)
print("CONFIG LOADED:")
print(f"  ENV: {settings.env}")
print(f"  SERPAPI_KEY: {'[OK]' if settings.serpapi_key else '[NO]'}")
print(f"  HIBP_API_KEY: {'[OK]' if settings.hibp_api_key else '[NO]'}")
print(f"  SYNTHETIC_MODE: {settings.synthetic_mode}")
print(f"  OFFLINE_MODE: {settings.offline_mode}")
print("=" * 50)
