from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routers import auth
from .routers import selfscan
from .routers import image
from .services.cleanup import start_scheduler
from .core.config import settings
from .core.database import init_db
from .middleware import AuditAndRateLimitMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="Dijital Ayak Izi API", version="0.1.0")

    # Uygulama istek almadan once tablolar olussun
    init_db()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(AuditAndRateLimitMiddleware, rate_limit_per_minute=60)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(selfscan.router, tags=["selfscan"])
    app.include_router(image.router, tags=["image"])
    
    # Static files (HTML UI)
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/")
    def read_root():
        static_index = os.path.join(static_dir, "index.html")
        if os.path.exists(static_index):
            return FileResponse(static_index)
        return {"message": "API running - visit /docs"}

    # background cleanup scheduler'i baslat
    start_scheduler()

    return app


app = create_app()


