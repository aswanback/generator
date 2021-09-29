import colorsys
import random
from pathlib import Path
from typing import List, Tuple, Union

from PIL import Image

import config as config


def tile_images(
    image_paths: List[str],
    tile_size: Tuple[int, int],
    overlap: int,
    *,
    output_dir: str = None,
    output_as_list: bool,
    input_as_list: bool,
) -> Union[List[Image.Image], None]:
    output_images = []
    if not output_as_list:
        output_dir = Path(output_dir)

    for path in image_paths:
        if input_as_list:
            image = path
        else:
            path = Path(path)
            image = Image.open(path)
        width, height = image.size
        tile_width, tile_height = tile_size

        count = 0
        for i in range(0, width - overlap, tile_width - overlap):
            if i + tile_width > width:
                i = width - tile_width

            for j in range(0, height - overlap, tile_height - overlap):
                if j + tile_height > height:
                    j = height - tile_width

                tile = image.crop((i, j, i + tile_width, j + tile_height))
                if output_as_list:
                    output_images.append(tile)
                else:
                    tile.save(output_dir / f"{path.stem}_{count}{path.suffix}")
                count += 1

    return output_images if output_as_list else None


# Gets the RGB color of the shape or letter based on color number
def get_random_rgba(color: str) -> Tuple[int, int, int]:
    # Color = ['WHITE', 'BLACK', 'GRAY', 'RED', 'BLUE', 'GREEN', 'YELLOW', 'PURPLE', 'BROWN', 'ORANGE ']
    # TODO: color ranges
    color_num = config.COLORS.index(color)
    hue_range = [
        (0, 360),
        (0, 360),
        (0, 360),
        (-20, 20),
        (150, 260),
        (70, 150),
        (40, 70),
        (260, 340),
        (20, 40),
        (20, 40),
    ]
    std_sat = (40, 100)
    sat_range = [
        (0, 10),
        (0, 10),
        (0, 10),
        std_sat,
        std_sat,
        std_sat,
        std_sat,
        std_sat,
        (30, 60),
        (60, 100),
    ]
    std_light = (40, 80)
    light_range = [
        (80, 100),
        (0, 10),
        (10, 30),
        std_light,
        std_light,
        std_light,
        std_light,
        std_light,
        (40, 60),
        (60, 80),
    ]

    hue_low, hue_high = hue_range[color_num]
    sat_low, sat_high = sat_range[color_num]
    light_low, light_high = light_range[color_num]

    hue = random.randint(hue_low, hue_high)
    saturation = random.randint(sat_low, sat_high)
    lightness = random.randint(light_low, light_high)

    rgb = colorsys.hls_to_rgb(hue / 360, lightness / 100, saturation / 100)
    rgb = [int(i * 255) for i in rgb]
    rgb.append(255)  # add alpha
    return tuple(rgb)
