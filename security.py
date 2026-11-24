import ipaddress
import logging
import socket
from urllib.parse import urlparse

import psutil
from fastapi import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import MEMORY_THRESHOLD_PERCENT, RATE_LIMIT_DEFAULT

logger = logging.getLogger(__name__)

# Rate-limit par IP cliente
limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT_DEFAULT])


def is_safe_url(url: str) -> bool:
    """Bloque schémas exotiques, IP privées/loopback/link-local/etc."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return False

    try:
        info = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror:
        return False

    for _, _, _, _, sockaddr in info:
        try:
            addr = ipaddress.ip_address(sockaddr[0])
        except ValueError:
            return False
        if (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
            or addr.is_multicast
            or addr.is_unspecified
        ):
            return False
    return True


def ensure_resources() -> None:
    """Dependency FastAPI : renvoie 503 si la RAM est saturée."""
    mem = psutil.virtual_memory()
    if mem.percent >= MEMORY_THRESHOLD_PERCENT:
        logger.warning("Mémoire critique : %.1f%% utilisés", mem.percent)
        raise HTTPException(
            status_code=503,
            detail="Server is under heavy load. Please try again shortly.",
        )