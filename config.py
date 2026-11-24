import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"

# Polices : d'abord la police embarquée, puis fallbacks système
DEFAULT_FONT_PATH = FONTS_DIR / "DejaVuSans.ttf"
FONT_CANDIDATES = [
    str(DEFAULT_FONT_PATH),
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "C:/Windows/Fonts/arial.ttf",
]

# Sécurité / limites
MAX_IMAGE_BYTES = int(os.getenv("MAX_IMAGE_BYTES", str(10 * 1024 * 1024)))  # 10 MiB
MAX_IMAGE_PIXELS = int(os.getenv("MAX_IMAGE_PIXELS", "20000000"))            # 20 MP
DOWNLOAD_TIMEOUT = float(os.getenv("DOWNLOAD_TIMEOUT", "15"))
PROXY_FALLBACK = os.getenv("PROXY_FALLBACK", "https://wsrv.nl/?url=")

MEMORY_THRESHOLD_PERCENT = float(os.getenv("MEMORY_THRESHOLD_PERCENT", "85"))
RATE_LIMIT_DEFAULT = os.getenv("RATE_LIMIT_DEFAULT", "30/minute")

API_VERSION = "1.1.0"