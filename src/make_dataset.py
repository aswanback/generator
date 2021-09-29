import pathlib
import random
import time
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tqdm import tqdm

import config
from individual_shapes import SHAPE_TO_MAKER
from utils import get_random_rgba


def get_shape(
    shape_size: int, shape_type: str, shape_color: Tuple[int, int, int]
) -> Image.Image:
    shape_func = SHAPE_TO_MAKER[shape_type]

    image = Image.new("RGBA", (shape_size, shape_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    shape_func(draw, shape_color, shape_size, (shape_size // 2, shape_size // 2))

    return image


def plant_alphanumeric(
    shape: Image.Image,
    alphanumeric: str,
    alpha_color: Tuple[int, int, int],
    font_file: Path,
    font_scalar: float,
) -> Image.Image:

    font = ImageFont.truetype(str(font_file), int(font_scalar * shape.height))
    draw = ImageDraw.Draw(shape)
    font_width, font_height = draw.textsize(alphanumeric, font=font)

    place_x, place_y = (shape.width - font_width) / 2, (shape.height - font_height) / 2
    place_y -= font_height * 0.21  # magic

    draw.text((place_x, place_y), alphanumeric, alpha_color, font=font)

    return shape


class Target:
    bbox_annotation = None

    def __init__(
        self,
        shape_size: int,
        shape_type: str,
        shape_color: Tuple[int, int, int],
        alphanumeric: str,
        alphanumeric_color: Tuple[int, int, int],
        font_file: pathlib.Path,
        font_scalar: float,
        degrees_shape: int,
        degrees_alphanumeric: int,
    ):
        self.shape_type = shape_type

        base_shape = get_shape(shape_size, shape_type, shape_color)

        base_shape = base_shape.rotate(degrees_shape, expand=1, fillcolor=(0, 0, 0, 0))
        base_shape = base_shape.crop(base_shape.getbbox())

        image = plant_alphanumeric(
            base_shape, alphanumeric, alphanumeric_color, font_file, font_scalar
        )

        image = image.rotate(degrees_alphanumeric, expand=1, fillcolor=(0, 0, 0, 0))
        self.image = image.crop(image.getbbox())

    @classmethod
    def generate_random(cls):
        shape_type = random.choice(config.SHAPES)
        shape_color, alphanumeric_color = random.sample(config.COLORS, 2)
        shape_color = get_random_rgba(shape_color)
        alphanumeric = random.choice(config.ALPHANUMERICS)
        alphanumeric_color = get_random_rgba(alphanumeric_color)
        font_file = random.choice(config.FONTS)
        font_scalar = random.uniform(*config.FONT_SCALAR_RANGE)
        shape_size = random.randint(*config.SHAPE_SIZE_RANGE)
        degrees_shape, degrees_alphanumeric = random.randint(0, 360), random.randint(
            0, 360
        )
        return cls(
            shape_size,
            shape_type,
            shape_color,
            alphanumeric,
            alphanumeric_color,
            font_file,
            font_scalar,
            degrees_shape,
            degrees_alphanumeric,
        )

    def write_out(self, output_dir, file_name):
        shape_index = config.SHAPES.index(self.shape_type)
        if config.DEBUG:
            self.image.show()
            time.sleep(5)
        else:
            with open(output_dir / (file_name + ".txt"), "w") as f:
                f.write(
                    str(shape_index)
                    + " "
                    + " ".join(map(str, list(self.bbox_annotation)))
                )

            self.image.save(output_dir / (file_name + ".jpeg"), "JPEG")


def make_dataset(num_to_generate: int, output_dir: Path, random_seed: int):
    random.seed(random_seed)
    output_dir.mkdir(exist_ok=True)

    background_images = [
        background_image for background_image in config.BACKGROUNDS_DIR.rglob("*")
    ]

    for i in tqdm(range(num_to_generate)):
        target = Target.generate_random()
        background = random.choice(background_images)

        image, bbox = paste_on_background(target.image, background)

        target.bbox_annotation = bbox
        target.image = image

        target.write_out(output_dir, f"image_{i}")


def paste_on_background(shape, background):
    background_image = Image.open(background)
    width, height = background_image.size

    place_x, place_y = int(random.uniform(0, width - shape.width)), int(
        random.uniform(0, height - shape.height)
    )
    x1, y1, x2, y2 = shape.getbbox()

    background_around_shape = background_image.crop(
        (x1 + place_x, y1 + place_y, x2 + place_x, y2 + place_y)
    )
    background_around_shape.paste(shape, (0, 0), shape)
    background_around_shape = background_around_shape.filter(
        ImageFilter.MedianFilter(3)
    )
    background_image.paste(background_around_shape, (place_x, place_y))

    place_x += (x2 - x1) / 2
    place_y += (y2 - y1) / 2
    place_x /= width
    place_y /= height

    w = (x2 - x1) / width
    h = (y2 - y1) / height

    return background_image, (place_x, place_y, w, h)


if __name__ == "__main__":
    make_dataset(config.NUMBER_TO_GENERATE, config.OUTPUT_DIR, config.RANDOM_SEED)
