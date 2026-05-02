import json
import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
DEFAULT_DATABASE_URL = "postgresql+psycopg2://movie_user:movie_password@db:5432/movie_booking"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def parse_origins(value: str | None) -> list[str]:
    if not value:
        return [
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:8080",
            "http://localhost:8080",
        ]
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    return [origin.strip() for origin in value.split(",") if origin.strip()]


load_env_file(ENV_PATH)


@dataclass(frozen=True)
class Settings:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str
    allowed_origins: list[str]
    host: str
    port: int
    debug: bool
    auto_create_tables: bool
    environment: str
    default_admin_email: str
    default_admin_password: str


settings = Settings(
    secret_key=os.getenv("SECRET_KEY", "change-me-in-production"),
    algorithm=os.getenv("ALGORITHM", "HS256"),
    access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
    database_url=os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL),
    allowed_origins=parse_origins(os.getenv("ALLOWED_ORIGINS")),
    host=os.getenv("HOST", "127.0.0.1"),
    port=int(os.getenv("PORT", "8000")),
    debug=parse_bool(os.getenv("DEBUG"), True),
    auto_create_tables=parse_bool(
        os.getenv("AUTO_CREATE_TABLES"),
        os.getenv("DATABASE_URL") is None,
    ),
    environment=os.getenv("ENVIRONMENT", "development").lower(),
    default_admin_email=os.getenv("DEFAULT_ADMIN_EMAIL", "admin@quickshow.local"),
    default_admin_password=os.getenv("DEFAULT_ADMIN_PASSWORD", "AdminPass123!"),
)
