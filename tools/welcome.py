import io
import math
from typing import Literal

from PIL import Image, ImageDraw

import helpers

Style = Literal["square", "round", "hex", "star", "heart"]
_STYLES: tuple[Style, ...] = ("square", "round", "hex", "star", "heart")


def _avatar_mask(style: Style, size: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    c = size // 2
    r = size // 2 - 2

    if style == "round":
        draw.ellipse((2, 2, size - 2, size - 2), fill=255)
    elif style == "hex":
        pts = [
            (c + r * math.cos(math.pi / 3 * i + math.pi / 6),
             c + r * math.sin(math.pi / 3 * i + math.pi / 6))
            for i in range(6)
        ]
        draw.polygon(pts, fill=255)
    elif style == "star":
        pts = []
        for i in range(10):
            rad = r if i % 2 == 0 else r // 2
            ang = math.pi / 5 * i - math.pi / 2
            pts.append((c + rad * math.cos(ang), c + rad * math.sin(ang)))
        draw.polygon(pts, fill=255)
    elif style == "heart":
        rr = size // 4
        draw.ellipse((c - 2 * rr, rr, c, 3 * rr), fill=255)
        draw.ellipse((c, rr, c + 2 * rr, 3 * rr), fill=255)
        draw.polygon([(0, 2 * rr), (size, 2 * rr), (c, size - 2)], fill=255)
    else:  # square
        draw.rectangle((0, 0, size, size), fill=255)
    return mask


def generate_welcome(
    url: str,
    username: str,
    title: str = "Welcome",
    style: Style = "square",
) -> bytes:
    if style not in _STYLES:
        raise ValueError(f"Invalid style. Choose from: {', '.join(_STYLES)}")

    avatar_size = 200
    avatar = helpers.download_image(url).convert("RGBA").resize((avatar_size, avatar_size))
    avatar.putalpha(_avatar_mask(style, avatar_size))

    canvas = Image.new("RGBA", (800, 400), (30, 30, 40, 255))
    canvas.paste(avatar, (50, 100), avatar)

    draw = ImageDraw.Draw(canvas)
    title_font = helpers.load_font(48)
    name_font = helpers.load_font(36)
    draw.text((280, 130), title, fill="white", font=title_font)
    draw.text((280, 210), username, fill=(200, 200, 200), font=name_font)

    out = io.BytesIO()
    canvas.convert("RGB").save(out, format="PNG")
    return out.getvalue()