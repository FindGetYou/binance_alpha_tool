import logging
import sys
from typing import Optional

from backend.config import config


def setup_logging(level: Optional[str] = None) -> None:
    lvl = getattr(logging, (level or config.LOG_LEVEL).upper(), logging.INFO)
    # Root logger
    logging.basicConfig(
        level=lvl,
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
        stream=sys.stdout,
    )
    # Tweak uvicorn loggers if present
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.setLevel(lvl)


logger = logging.getLogger("app")
