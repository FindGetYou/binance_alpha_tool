"""
Centralized backend configuration.
Adjust values via environment variables or directly here.
"""
import os
from decimal import ROUND_HALF_UP

# Numeric precision
DECIMAL_PLACES: int = int(os.getenv("DECIMAL_PLACES", "8"))
ROUNDING_MODE = ROUND_HALF_UP  # round half up mode, shared by backend

# Proxy settings
USE_PROXY: bool = os.getenv("USE_PROXY", "true").lower() in {"1", "true", "yes"}
HTTP_PROXY: str = os.getenv("HTTP_PROXY", "http://127.0.0.1:33210")
SOCKS_HOST: str = os.getenv("SOCKS_HOST", "127.0.0.1")
SOCKS_PORT: int = int(os.getenv("SOCKS_PORT", "33211"))

# Rate limiting (simple in-memory)
RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "60"))

# HTTP client retry policy
RETRY_MAX_ATTEMPTS: int = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
RETRY_BACKOFF_BASE: float = float(os.getenv("RETRY_BACKOFF_BASE", "0.25"))  # seconds
RETRY_BACKOFF_FACTOR: float = float(os.getenv("RETRY_BACKOFF_FACTOR", "2.0"))

# Logging
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

# External APIs
BINANCE_REST_BASE: str = os.getenv("BINANCE_REST_BASE", "https://www.binance.com")

# If you have an Alpha tokens listing API, configure it here.
# When empty, service will fallback to local file or empty list.
ALPHA_TOKENS_API: str = os.getenv("ALPHA_TOKENS_API", "https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/cex/alpha/all/token/list")

# Trading symbol construction
ALPHA_SYMBOL_SUFFIX: str = os.getenv("ALPHA_SYMBOL_SUFFIX", "USDT")
DEFAULT_TRADES_LIMIT: int = int(os.getenv("DEFAULT_TRADES_LIMIT", "50"))
