"""
Script to test SHARP Memory Display
Author: Dmytro Zhovtobriukh
"""
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from sharpmemorydisplay import SharpMemoryDisplay


# Colors
BLACK = 0
WHITE = 255

# Parameters to Change
BORDER = 4
FONTSIZE = 24


def listify(img: Image):
    return np.packbits(
        np.asarray(img.rotate(180, expand=1)), axis=1
    ).flatten().tolist()


def create_image(width, height):
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    return image, draw


def empty_rectangle(draw: ImageDraw, color):
    w = 144
    h = 168

    draw.rectangle(
        (0, 0, w - 1, h - 1),
        outline=color,
        fill=color
    )


def test_rectangle(display: SharpMemoryDisplay) -> None:
    w = display.width
    h = display.height

    image, draw = create_image(w, h)

    for i in range(min(w, h) // (BORDER * 2)):
        draw.rectangle(
            (
                0 + BORDER * i,
                0 + BORDER * i,
                w - BORDER * i - 1,
                h - BORDER * i - 1
            ),
            outline=WHITE if (i % 2 == 0) else BLACK,
            fill=WHITE if (i % 2 == 0) else BLACK
        )
        display.dummy(listify(image))
        display.show()


def test_triangle(display: SharpMemoryDisplay) -> None:
    w = display.width
    h = display.height

    image, draw = create_image(w, h)

    empty_rectangle(draw, WHITE)

    x1, y1 = w // 2, 0
    x2, y2 = 0, h - 1
    x3, y3 = w - 1, h - 1

    draw.polygon(
        [(x1, y1), (x2, y2), (x3, y3)],
        outline=BLACK,
        fill=BLACK
    )

    # Lengths of sides of the triangle
    a = ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5
    b = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
    c = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    j = BORDER

    H = (b ** 2 - (a / 2) ** 2) ** 0.5
    k = 2 * j * b / a
    i = a / 2 - (H - k - j) * a / (2 * H)

    for o in range(min(w // int(i * 2), h // int(j + k))):

        draw.polygon(
            [
                (x1, y1 + k * o),
                (x2 + i * o, y2 - j * o),
                (x3 - i * o, y3 - j * o)
            ],
            outline=WHITE if (o % 2 == 1) else BLACK,
            fill=WHITE if (o % 2 == 1) else BLACK
        )
        display.dummy(listify(image))
        display.show()


def test_line(display: SharpMemoryDisplay) -> None:
    w = display.width
    h = display.height

    image, draw = create_image(w, h)

    # Upper left corner

    empty_rectangle(draw, WHITE)

    for i in range(h // (BORDER * 2)):
        draw.line(
            (0, 0, w - 1, BORDER * 2 * i),
            width=1,
            fill=BLACK
        )
        display.dummy(listify(image))
        display.show()

    for i in range(w // (BORDER * 2)):
        draw.line(
            (0, 0, w - BORDER * 2 * i - 1, h - 1),
            width=1,
            fill=BLACK
        )
        display.dummy(listify(image))
        display.show()

    # Upper right corner

    empty_rectangle(draw, WHITE)

    for i in range(h // (BORDER * 2)):
        draw.line(
            (w - 1, 0, 0, BORDER * 2 * i),
            width=1,
            fill=BLACK
        )
        display.dummy(listify(image))
        display.show()

    for i in range(w // (BORDER * 2)):
        draw.line(
            (w - 1, 0, BORDER * 2 * i, h - 1),
            width=1,
            fill=BLACK
        )
        display.dummy(listify(image))
        display.show()

    # Lower right corner

    empty_rectangle(draw, WHITE)

    for i in range(h // (BORDER * 2)):
        draw.line(
            (w - 1, h - 1, 0, h - BORDER * 2 * i - 1),
            width=1,
            fill=BLACK
        )
        display.dummy(listify(image))
        display.show()

    for i in range(w // (BORDER * 2)):
        draw.line(
            (w - 1, h - 1, BORDER * 2 * i, 0),
            width=1,
            fill=BLACK
        )
        display.dummy(listify(image))
        display.show()

    # Lower left corner

    empty_rectangle(draw, WHITE)

    for i in range(h // (BORDER * 2)):
        draw.line(
            (0, h - 1, w - 1, h - BORDER * 2 * i - 1),
            width=1,
            fill=BLACK
        )
        display.dummy(listify(image))
        display.show()

    for i in range(w // (BORDER * 2)):
        draw.line(
            (0, h - 1, w - BORDER * 2 * i - 1, 0),
            width=1,
            fill=BLACK
        )
        display.dummy(listify(image))
        display.show()


def test_text(display: SharpMemoryDisplay) -> None:
    w = display.width
    h = display.height

    image, draw = create_image(w, h)

    empty_rectangle(draw, WHITE)

    font_sizes = (9, 10, 11, 12, 14, 16, 18, 20, 22, 24)

    text = "abcdefghi"

    y = 0

    for font_size in font_sizes:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 
            font_size
        )
        (font_width, _) = font.getsize(text)
        (c_w, _) = (w // 2 - 1, y)
        draw.text(
            (c_w - font_width // 2, y),
            text,
            font=font,
            fill=BLACK,
        )
        y += font_size
        display.dummy(listify(image))
        display.show()
    time.sleep(1)


def main():
    display = SharpMemoryDisplay(1, 0)

    w = display.width
    h = display.height

    # Initialize display with the white color
    display.dummy([WHITE] * (w * h // 8))
    display.show()

    try:
        test_text(display)
        test_rectangle(display)
        test_line(display)
        test_triangle(display)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
        with open('log.txt', 'w', encoding='utf-8') as f:
            f.write(str(e))
    finally:
        del display


if __name__ == "__main__":
    main()
