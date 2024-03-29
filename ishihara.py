import math
import random
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageColor
import numpy as np


FONT = 'Rubik-Bold.ttf'


def color(c):
    return ImageColor.getcolor(c, 'RGB')


# Dict with tuples items formatted - ([#COLORS_ON], [#COLORS_OFF])
COLORS = dict()

COLORS['Yellow|Green'] = ([color('#F9BB82'), color('#EBA170'), color('#FCCD84')],
                          [color('#9CA594'), color('#ACB4A5'), color('#BBB964'),
                           color('#D7DAAA'), color('#E5D57D'), color('#D1D6AF')]
                          )

COLORS['Green|Red'] = ([color('#b6b87c'), color('#e3da73'), color('#b0ab60')],
                       [color('#ef845a'), color('#ffc68c'), color('#ef845a')]
                       )

COLORS['Pink|Black'] = ([color('#f79087'), color('#f26969'), color('#d8859d'),
                         color('#f79087')],
                        [color('#5a4e46'), color('#7b6b63'), color('#9c9c84')]
                        )

COLORS['Green|Yellow+Red'] = ([color('#b6b87c'), color('#e3da73'), color('#b0ab60')],
                              [color('#ef845a'), color('#ffc68c'), color('#ef845a'),
                               color('#fff36b'), color('#ffbd52')]
                              )


def generate_circle(image_width, image_height, min_diameter, max_diameter):
    radius = random.triangular(min_diameter, max_diameter,
                               max_diameter * 0.8 + min_diameter * 0.2) / 2

    angle = random.uniform(0, math.pi * 2)
    distance_from_center = random.uniform(0, min(image_width, image_height) * 0.5 - radius)
    x = image_width * 0.5 + math.cos(angle) * distance_from_center
    y = image_height * 0.5 + math.sin(angle) * distance_from_center

    return x, y, radius


def circle_avaible(circle, width, height, radius):
    x, y, r = circle
    return (width/2 - x)**2 + (height/2 - y)**2 < radius**2


def overlaps_motive(image, circle):
    x, y, r = circle
    return np.mean(image.crop((x-r, y-r, x+r, y+r))) > 127


def circle_intersection(circle1, circle2):
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    return (x2 - x1)**2 + (y2 - y1)**2 < (r2 + r1)**2


def circle_draw(draw_image, circle, image, schema):
    fill_colors = COLORS[schema][0] if overlaps_motive(image, circle) else COLORS[schema][1]
    fill_color = random.choice(fill_colors)

    x, y, r = circle
    draw_image.ellipse((x - r, y - r, x + r, y + r),
                       fill=fill_color,
                       outline=fill_color)


def create_image(text='only love is real', width=1024, height=1024):
    text = '\n'.join(text.split())
    text = text.upper()

    image_text = Image.new('L', (width, height), 'white')
    writer = ImageDraw.Draw(image_text)

    font_size = 1
    font = ImageFont.truetype(FONT, size=font_size)
    while (writer.textbbox((0, 0), text, font=font)[2] < 0.9 * width and
           writer.textbbox((0, 0), text, font=font)[3] < 0.9 * height):
        font_size += 1
        font = ImageFont.truetype(FONT, size=font_size)

    _, _, w, h = writer.textbbox((0, 0), text, font=font)

    writer.text(((width-w)/2, (height-h)/2), text, font=font, fill='black', align='center')

    image = Image.new('RGB', (width, height), 'white')
    draw_image = ImageDraw.Draw(image)

    min_radius = min(width, height) / min(100 + 15 * len(text), 250)
    max_radius = min(width, height) / min(100 + 10 * len(text), 200)

    color_schema = random.choice(list(COLORS.keys()))
    circles = []
    try:
        start = datetime.datetime.now()
        big_radius = min(width, height) / 2
        x = max_radius
        new_line = []
        while x < width:
            y = max_radius
            last_line = new_line.copy()
            new_line = []
            while y < height:
                radius = random.triangular(min_radius, max_radius,
                                           max_radius * 0.8 + min_radius * 0.2)
                circle = (x + random.triangular(-max_radius, max_radius), y, radius)

                if (circle_avaible(circle, width, height, big_radius) and
                        not any(circle_intersection(circle, circle2) for circle2 in last_line) and
                        not any(circle_intersection(circle, circle2) for circle2 in new_line)):
                    new_line.append(circle)
                    circles.append(circle)
                    circle_draw(draw_image, circle, image_text, color_schema)

                    print('Total circles {}'.format(len(circles)))

                y += random.triangular(min_radius, max_radius,
                                       max_radius * 0.8 + min_radius * 0.2)

                if (datetime.datetime.now() - start).total_seconds() > 300:
                    print('Timer call')
                    break

            x += random.triangular(min_radius, max_radius,
                                   max_radius * 0.8 + min_radius * 0.2)

    except (KeyboardInterrupt, SystemExit):
        pass

    #image.save('res.png')
    image.show()
    return image


if __name__ == '__main__':
    create_image('let\'s dance')
