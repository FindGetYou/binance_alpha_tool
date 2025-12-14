import time
import uuid
import logging
from collections import deque, defaultdict
from typing import Callable, Deque, Dict, Tuple

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from backend.config import config

logger = logging.getLogger("app.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs method, path, status, duration. Injects X-Request-ID if missing."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        start = time.perf_counter()
        try:
            response: Response = await call_next(request)
        except Exception:
            # Unhandled exceptions will be logged by error handler
            raise
        finally:
            duration_ms = (time.perf_counter() - start) * 1000.0
            logger.info(
                "%s %s -> %sms",
                request.method,
                request.url.path,
                f"{duration_ms:.2f}",
            )
        # Propagate request id
        response.headers.setdefault("X-Request-ID", req_id)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple sliding window limiter per (ip, path)."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.window = config.RATE_LIMIT_WINDOW_SECONDS
        self.limit = config.RATE_LIMIT_MAX_REQUESTS
        self.buckets: Dict[Tuple[str, str], Deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        key = (self._client_ip(request), request.url.path)
        now = time.monotonic()
        q = self.buckets[key]
        # Drop expired
        cutoff = now - self.window
        while q and q[0] < cutoff:
            q.popleft()
        if len(q) >= self.limit:
            headers = {
                "Retry-After": str(int(self.window)),
                "X-RateLimit-Limit": str(self.limit),
                "X-RateLimit-Remaining": "0",
            }
            return Response("Too Many Requests", status_code=429, headers=headers)
        q.append(now)
        remaining = max(0, self.limit - len(q))
        response: Response = await call_next(request)
        response.headers.setdefault("X-RateLimit-Limit", str(self.limit))
        response.headers.setdefault("X-RateLimit-Remaining", str(remaining))
        return response

    @staticmethod
    def _client_ip(request: Request) -> str:
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()
        return request.client.host if request.client else "-"
