import io
import logging

import requests
from PIL import Image, ImageColor, ImageFont

from config import (
    DOWNLOAD_TIMEOUT,
    FONT_CANDIDATES,
    MAX_IMAGE_BYTES,
    MAX_IMAGE_PIXELS,
    PROXY_FALLBACK,
)
from security import is_safe_url

logger = logging.getLogger(__name__)

# Protection contre les "decompression bombs"
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, TypeError):
            continue
    logger.warning("Aucune police TrueType trouvée, fallback police bitmap")
    return ImageFont.load_default()


def parse_color(value: str) -> tuple[int, int, int]:
    """Lève ValueError explicite si la couleur est invalide."""
    try:
        rgb = ImageColor.getrgb(value)
    except ValueError as exc:
        raise ValueError(f"Invalid color value: {value!r}") from exc
    return rgb[:3]


def _fetch(url: str) -> bytes:
    with requests.get(url, timeout=DOWNLOAD_TIMEOUT, stream=True) as resp:
        resp.raise_for_status()
        ctype = resp.headers.get("Content-Type", "").lower()
        if ctype and not ctype.startswith("image/"):
            raise ValueError(f"URL did not return an image ({ctype})")

        buf = bytearray()
        for chunk in resp.iter_content(chunk_size=64 * 1024):
            if not chunk:
                continue
            buf.extend(chunk)
            if len(buf) > MAX_IMAGE_BYTES:
                raise ValueError(f"Image exceeds {MAX_IMAGE_BYTES} bytes")
        return bytes(buf)


def download_image(url: str) -> Image.Image:
    """Télécharge avec validation SSRF + fallback proxy."""
    if not is_safe_url(url):
        raise ValueError("URL is not allowed (unsafe or private address)")

    data: bytes | None = None
    try:
        data = _fetch(url)
    except (requests.RequestException, ValueError) as exc:
        logger.info("Direct download failed (%s) — trying proxy", exc)
        proxy_url = PROXY_FALLBACK + url
        if not is_safe_url(proxy_url):
            raise ValueError("Proxy URL rejected")
        data = _fetch(proxy_url)

    try:
        img = Image.open(io.BytesIO(data))
        img.load()
        return img
    except Exception as exc:
        raise ValueError("Downloaded file is not a valid image") from exc


def wrap_text(text: str, font, max_width: int) -> list[str]:
    """Wrap propre, casse les mots trop longs."""
    if not text.strip():
        return [""]
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if font.getlength(candidate) <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
        # mot trop long : on casse
        while font.getlength(word) > max_width:
            cut = len(word)
            while cut > 1 and font.getlength(word[:cut]) > max_width:
                cut -= 1
            lines.append(word[:cut])
            word = word[cut:]
        current = word
    if current:
        lines.append(current)
    return lines or [""]