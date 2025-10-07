from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.sqlite_url, connect_args={"check_same_thread": False} if settings.sqlite_url.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    # Modelleri import ederek metadata'ya kaydolmalarini sagla
    from ..models import user as _user  # noqa: F401
    from ..models import audit as _audit  # noqa: F401
    Base.metadata.create_all(bind=engine)


