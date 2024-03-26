import math
import random
import sys

from PIL import Image, ImageDraw, ImageFont, ImageColor
import numpy as np

BACKGROUND = (255, 255, 255)

FONT = 'Rubik.ttf'

color = lambda c: ImageColor.getcolor(c, 'RGB') #((c >> 16) & 255, (c >> 8) & 255, c & 255)

# Dict with tuples items formatted - ([#COLORS_ON], [#COLORS_OFF])
COLORS = {}

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


def main(text='only love is real', width=1024, height=1024):
    text = '\n'.join(text.split())
    text = text.upper()

    image_text = Image.new('L', (width, height), 'white')
    writer = ImageDraw.Draw(image_text)

    fontsize = 1
    font = ImageFont.truetype(FONT, size=fontsize)
    while writer.textbbox((0, 0), text, font=font)[2] < 0.7 * width and writer.textbbox((0, 0), text, font=font)[3] < 0.7 * height:
        fontsize += 1
        font = ImageFont.truetype(FONT, size=fontsize)

    _, _, w, h = writer.textbbox((0, 0), text, font=font)

    writer.text(((width-w)/2, (height-h)/2), text, font=font, fill='black', align='center')

    image2 = Image.new('RGB', (width, height), BACKGROUND)
    draw_image = ImageDraw.Draw(image2)

    min_diameter = min(width, height) / (50+10*len(text))
    max_diameter = min(width, height) / (50+5*len(text))

    color_schema = random.choice(list(COLORS.keys()))
    circles = []
    tries = 0
    try:
        while tries < 300:
            tries += 1
            circle = generate_circle(width, height, min_diameter, max_diameter)
            if not any(circle_intersection(circle, circle2) for circle2 in circles):
                circles.append(circle)
                circle_draw(draw_image, circle, image_text, color_schema)

                print('Total circles {}.  {}'.format(len(circles), tries))
                tries = 0
    except (KeyboardInterrupt, SystemExit):
        pass

    image2.save('res.png')
    image2.show()

if __name__ == '__main__':
    main(sys.argv[1])
