import io
import os

# Doit précéder l'import de main
os.environ.setdefault("RATE_LIMIT_DEFAULT", "10000/minute")
os.environ.setdefault("MEMORY_THRESHOLD_PERCENT", "99.9")

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_image_png() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (120, 80), "red").save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def fake_download(sample_image_png, monkeypatch):
    """Remplace helpers.download_image pour éviter les appels réseau."""
    def _fake(url: str):
        return Image.open(io.BytesIO(sample_image_png))
    monkeypatch.setattr("helpers.download_image", _fake)