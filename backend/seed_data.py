from app.auth import get_password_hash
from app.config import settings
from app.database import SessionLocal
from app.models import Theater, User


DEFAULT_THEATERS = [
    {"name": "QuickShow Downtown", "location": "Downtown Mall"},
    {"name": "QuickShow Riverside", "location": "Riverside Avenue"},
    {"name": "QuickShow Grand Hall", "location": "Central Square"},
]


def ensure_default_admin() -> None:
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.default_admin_email).first()
        password_hash = get_password_hash(settings.default_admin_password)

        if admin is None:
            admin = User(
                email=settings.default_admin_email,
                hashed_password=password_hash,
                role="admin",
            )
            db.add(admin)
        else:
            admin.hashed_password = password_hash
            admin.role = "admin"

        db.commit()
    finally:
        db.close()


def upsert_theaters() -> None:
    db = SessionLocal()
    try:
        for payload in DEFAULT_THEATERS:
            theater = db.query(Theater).filter(Theater.name == payload["name"]).first()
            if theater is None:
                db.add(Theater(**payload))
                continue

            theater.location = payload["location"]

        db.commit()
    finally:
        db.close()


def seed_initial_data() -> None:
    from add_movies import upsert_movies

    ensure_default_admin()
    upsert_theaters()
    upsert_movies()
