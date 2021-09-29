from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent

# MODE
DEBUG = False

# ENTROPY
RANDOM_SEED = 343433

# OUTPUT GENERATED
NUMBER_TO_GENERATE = 20
OUTPUT_DIR = ROOT_DIR / "generated_dataset"

# FONTS
FONTS_DIR = ROOT_DIR / "fonts"
FONTS = list(FONTS_DIR.rglob("*"))
FONT_SCALAR_RANGE = (0.6, 0.65)

# BACKGROUNDS
BACKGROUNDS_DIR = ROOT_DIR / "backgrounds"

# SHAPES
SHAPE_SIZE_RANGE = (39, 40)
SHAPES = [
    "circle",
    "semicircle",
    "quarter_circle",
    "triangle",
    "square",
    "rectangle",
    "trapezoid",
    "pentagon",
    "hexagon",
    "octagon",
    "star",
    "cross",
]

# ORIENTATION
ORIENTATION = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# COLORS
COLORS = [
    "white",
    "black",
    "gray",
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "brown",
    "orange",
]

# ALPHANUMERICS
ALPHANUMERICS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
]
