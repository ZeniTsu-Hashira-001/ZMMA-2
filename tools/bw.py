import io

import helpers


def generate_bw(url: str) -> bytes:
    img = helpers.download_image(url).convert("L").convert("RGB")
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()