import io

from PIL import Image, ImageDraw

import helpers


def generate_brat(text: str, fg: str = "black", bg: str = "white", size: int = 512) -> bytes:
    fg_color = helpers.parse_color(fg)
    bg_color = helpers.parse_color(bg)

    image = Image.new("RGB", (size, size), bg_color)
    draw = ImageDraw.Draw(image)

    max_w = size - 40
    max_h = size - 40

    # Cherche la plus grande police qui rentre
    chosen = None
    font_size = 80
    while font_size >= 14:
        font = helpers.load_font(font_size)
        lines = helpers.wrap_text(text, font, max_w)
        line_h = font_size + 6
        total_h = line_h * len(lines)
        widest = max((font.getlength(l) for l in lines), default=0)
        if widest <= max_w and total_h <= max_h:
            chosen = (font, lines, line_h, total_h)
            break
        font_size -= 4

    if chosen is None:
        font = helpers.load_font(14)
        lines = helpers.wrap_text(text, font, max_w)
        line_h = 20
        chosen = (font, lines, line_h, line_h * len(lines))

    font, lines, line_h, total_h = chosen
    y = (size - total_h) // 2
    for line in lines:
        lw = font.getlength(line)
        x = (size - lw) // 2
        draw.text((x, y), line, fill=fg_color, font=font)
        y += line_h

    out = io.BytesIO()
    image.save(out, format="PNG")
    return out.getvalue()