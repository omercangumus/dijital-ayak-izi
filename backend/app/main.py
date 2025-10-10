from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routers import auth
from .routers import selfscan
from .routers import image
from .routers import profile_analysis
from .routers import osint
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
    app.include_router(profile_analysis.router, prefix="/api/profile-analysis", tags=["profile-analysis"])
    app.include_router(osint.router, prefix="/api/osint", tags=["osint"])
    
    # Static files (React build)
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/")
    def read_root():
        # Check if React build exists
        react_index = os.path.join(static_dir, "dist", "index.html")
        if os.path.exists(react_index):
            return FileResponse(react_index)
        
        # Fallback to old HTML
        static_index = os.path.join(static_dir, "index.html")
        if os.path.exists(static_index):
            return FileResponse(static_index)
        
        return {"message": "API running - visit /docs"}
    
    @app.get("/{full_path:path}")
    def serve_react_app(full_path: str):
        """Serve React app for all routes"""
        react_index = os.path.join(static_dir, "dist", "index.html")
        if os.path.exists(react_index):
            return FileResponse(react_index)
        return {"message": "React app not built - run 'npm run build' in frontend directory"}

    # background cleanup scheduler'i baslat
    start_scheduler()

    return app


app = create_app()


