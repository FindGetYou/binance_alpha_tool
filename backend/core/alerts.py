"""
Alerts stub. Replace implementations with integrations (Sentry, Slack, email) later.
"""
import logging
import traceback
from typing import Optional

logger = logging.getLogger("alerts")


def alert_error(msg: str, exc: Optional[BaseException] = None) -> None:
    if exc is not None:
        logger.error("%s\n%s", msg, "".join(traceback.format_exception(exc)))
    else:
        logger.error("%s", msg)
