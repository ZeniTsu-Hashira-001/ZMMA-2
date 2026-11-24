import io

from PIL import ImageOps

import helpers


def generate_reverse(url: str) -> bytes:
    img = helpers.download_image(url).convert("RGB")
    img = ImageOps.mirror(img)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()