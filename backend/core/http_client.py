import asyncio
import logging
import os
from typing import Any

import httpx

from backend.config import config

logger = logging.getLogger("app.http")


def _apply_env_proxies() -> None:
    """Configure proxies via environment variables for broad httpx compatibility.
    httpx honors HTTP(S)_PROXY when trust_env=True (default).
    """
    if not config.USE_PROXY:
        return
    if config.HTTP_PROXY:
        proxy = config.HTTP_PROXY.strip()
        # Ensure scheme present for env proxies
        if '://' not in proxy:
            proxy = f"http://{proxy}"
        os.environ.setdefault("HTTP_PROXY", proxy)
        os.environ.setdefault("HTTPS_PROXY", proxy)


def get_async_client(**kwargs) -> httpx.AsyncClient:
    # Use env proxies for compatibility across httpx versions
    _apply_env_proxies()
    timeout = kwargs.pop("timeout", 10.0)
    return httpx.AsyncClient(timeout=timeout, trust_env=True, **kwargs)


async def request_with_retries(client: httpx.AsyncClient, method: str, url: str, *,
                               max_attempts: int = None, backoff_base: float = None,
                               backoff_factor: float = None, **kwargs) -> httpx.Response:
    attempts = max_attempts or config.RETRY_MAX_ATTEMPTS
    base = backoff_base or config.RETRY_BACKOFF_BASE
    factor = backoff_factor or config.RETRY_BACKOFF_FACTOR

    for i in range(1, attempts + 1):
        try:
            resp = await client.request(method, url, **kwargs)
            if resp.status_code >= 500:
                raise httpx.HTTPStatusError("server error", request=resp.request, response=resp)
            return resp
        except (httpx.TransportError, httpx.HTTPStatusError) as e:
            if i == attempts:
                logger.error("HTTP failed after %s attempts: %s %s", i, method, url)
                raise
            delay = base * (factor ** (i - 1))
            await asyncio.sleep(delay)
