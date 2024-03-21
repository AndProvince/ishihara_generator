import math
import random
import sys

from PIL import Image, ImageDraw, ImageFont
import numpy as np

BACKGROUND = 'white' #(255, 255, 255)

color = lambda c: ((c >> 16) & 255, (c >> 8) & 255, c & 255)

COLORS_ON = [
    color(0xF9BB82), color(0xEBA170), color(0xFCCD84)
]
COLORS_OFF = [
    color(0x9CA594), color(0xACB4A5), color(0xBBB964),
    color(0xD7DAAA), color(0xE5D57D), color(0xD1D6AF)
]


def generate_circle(image_width, image_height, min_diameter, max_diameter):
    radius = random.triangular(min_diameter, max_diameter,
                               max_diameter * 0.8 + min_diameter * 0.2) / 2

    angle = random.uniform(0, math.pi * 2)
    distance_from_center = random.uniform(0, min(image_width, image_height) * 0.5 - radius)
    x = image_width * 0.5 + math.cos(angle) * distance_from_center
    y = image_height * 0.5 + math.sin(angle) * distance_from_center

    return x, y, radius


def overlaps_motive(image, circle):
    x, y, r = circle
    return np.mean(image.crop((x-r, y-r, x+r, y+r))) > 127
    # return image.getpixel((x, y)) > 127


def circle_intersection(circle1, circle2):
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    return (x2 - x1)**2 + (y2 - y1)**2 < (r2 + r1)**2


def circle_draw(draw_image, circle, image):
    fill_colors = COLORS_ON if overlaps_motive(image, circle) else COLORS_OFF
    fill_color = random.choice(fill_colors)

    x, y, r = circle
    draw_image.ellipse((x - r, y - r, x + r, y + r),
                       fill=fill_color,
                       outline=fill_color)


def main(text='ЛОХ\nЭТО\nСУДЬБА', width=1024, height=1024):
    text = text.upper()

    image1 = Image.new('L', (width, height), 'white')
    writer = ImageDraw.Draw(image1)

    fontsize = 1
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=fontsize)
    while writer.textbbox((0, 0), text, font=font)[2] < 0.9 * width and writer.textbbox((0, 0), text, font=font)[3] < 0.9 * height:
    # while font.getlength(text) < min(width, height):
        fontsize += 1
        font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=fontsize)

    _, _, w, h = writer.textbbox((0, 0), text, font=font)

    writer.text(((width-w)/2, (height-h)/2), text, font=font, fill='black', align='center')


    image2 = Image.new('RGB', (width, height), BACKGROUND)
    draw_image = ImageDraw.Draw(image2)

    min_diameter = min(width, height) / 120
    max_diameter = min(width, height) / 60

    circles = []
    tries = 0
    try:
        while tries < 300:
            tries += 1
            circle = generate_circle(width, height, min_diameter, max_diameter)
            if not any(circle_intersection(circle, circle2) for circle2 in circles):
                circles.append(circle)
                circle_draw(draw_image, circle, image1)

                print('Total circles {}.  {}'.format(len(circles), tries))
                tries = 0
    except (KeyboardInterrupt, SystemExit):
        pass

    image2.save('res.png')
    image2.show()
    #image1.show()

if __name__ == '__main__':
    main(sys.argv[1])
