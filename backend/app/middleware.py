import time
from collections import defaultdict
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .core.database import SessionLocal
from .services.audit import write_audit_log


class AuditAndRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit_per_minute: int = 60):
        super().__init__(app)
        self.rate_limit_per_minute = rate_limit_per_minute
        self.ip_hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        client_ip = request.client.host if request.client else "unknown"

        now = time.time()
        window_start = now - 60
        hits = self.ip_hits[client_ip]
        # temizle
        self.ip_hits[client_ip] = [t for t in hits if t >= window_start]
        if len(self.ip_hits[client_ip]) >= self.rate_limit_per_minute:
            return Response("Too Many Requests", status_code=429)
        self.ip_hits[client_ip].append(now)

        start = time.time()
        response = await call_next(request)
        duration_ms = int((time.time() - start) * 1000)

        try:
            db = SessionLocal()
            try:
                write_audit_log(
                    db=db,
                    action=f"{request.method} {request.url.path}",
                    ip=client_ip,
                    detail=f"status={response.status_code} durationMs={duration_ms}",
                    user_id=None,
                )
            finally:
                db.close()
        except Exception:
            # Audit yazimi kritik degil, tablo hazir degilse veya hata varsa yut
            pass

        return response


