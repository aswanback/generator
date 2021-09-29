import math
import operator


def circle(draw, color, size, center):
    draw.ellipse(
        (
            center[0] - size / 2,
            center[1] - size / 2,
            center[0] + size / 2,
            center[1] + size / 2,
        ),
        fill=color,
    )


def semicircle(draw, color, size, center):
    size = size / 2
    draw.pieslice(
        (
            center[0] - size,
            center[1] - size - size / 2,
            center[0] + size,
            center[1] + size - size / 2,
        ),
        start=0,
        end=180,
        fill=color,
    )


def quarter_circle(draw, color, size, center):
    size = size / 1.15
    draw.pieslice(
        (
            center[0] - size - size * 4 / 3 / 3.14159,
            center[1] - size - size * 4 / 3 / 3.14159,
            center[0] + size - size * 4 / 3 / 3.14159,
            center[1] + size - size * 4 / 3 / 3.14159,
        ),
        start=0,
        end=90,
        fill=color,
    )


def triangle(draw, color, size, center):
    _nsides(draw, color, size, center, 3)  # equilateral
    # Equilateral
    # w = size*2
    # h = w*math.sqrt(3)/2
    # # Right Triangle 1-1-sqrt(2)
    # w = size
    # h = w / 2
    # centroidy = h/6
    # draw.polygon(((center[0], center[1] + h / 2+centroidy), (center[0] - w / 2, center[1] - h / 2+centroidy),
    # (center[0] + w / 2, center[1] - h / 2+centroidy)), fill=color)


def square(draw, color, size, center):
    _nsides(draw, color, size, center, 4)
    # draw.rectangle((center[0] - size / 2, center[1] - size / 2, center[0] + size / 2, center[1] + size / 2),
    # fill=color)


def rectangle(draw, color, size, center):
    aspect = 0.8  # TODO: make rectangle aspect ratio random?
    draw.rectangle(
        (
            center[0] - size / 2,
            center[1] - size / 2 * aspect,
            center[0] + size / 2,
            center[1] + size / 2 * aspect,
        ),
        fill=color,
    )


def trapezoid(draw, color, size, center):
    d = size / 5  # offset width
    hh = size / 3  # half height
    hw = size / 2  # half width
    draw.polygon(
        (
            (center[0] - hw, center[1] + hh),
            (center[0] - hw + d, center[1] - hh),
            (center[0] + hw, center[1] - hh),
            (center[0] + hw - d, center[1] + hh),
        ),
        fill=color,
    )


def pentagon(draw, color, size, center):
    _nsides(draw, color, size, center, 5)


def hexagon(draw, color, size, center):
    _nsides(draw, color, size, center, 6)


def heptagon(draw, color, size, center):
    _nsides(draw, color, size, center, 7)


def octagon(draw, color, size, center):
    _nsides(draw, color, size, center, 8)


def star(draw, color, size, center):
    h = size / 5.9  # why? dont ask
    w = 2 / math.tan(36 * math.pi / 180) * h

    theta = 2 * 6 / 5 * 120 / 180 * math.pi
    theta2 = 4 * 6 / 5 * 120 / 180 * math.pi
    c, s = math.cos(theta), math.sin(theta)
    c2, s2 = math.cos(theta2), math.sin(theta2)
    off = 2 / math.sqrt(5 + 2 * math.sqrt(5)) / math.tan(36 * math.pi / 180)
    i = [(0, -2 * h + off * h), (w, off * h), (-w, off * h)]

    j = tuple([(c * x - s * y, s * x + c * y) for (x, y) in i])
    k = tuple([(c2 * x - s2 * y, s2 * x + c2 * y) for (x, y) in i])

    i = [tuple(map(operator.add, a, center)) for a in i]
    j = [tuple(map(operator.add, a, center)) for a in j]
    k = [tuple(map(operator.add, a, center)) for a in k]

    draw.polygon(i, fill=color)
    draw.polygon(j, fill=color)
    draw.polygon(k, fill=color)


def cross(draw, color, size, center):
    w = size / 2
    h = w / 3
    rect = ((-w, h), (w, -h))

    c, s = math.cos(math.pi / 2), math.sin(math.pi / 2)
    rect2 = tuple([(c * x - s * y, s * x + c * y) for (x, y) in rect])

    rect = [tuple(map(operator.add, a, center)) for a in rect]
    rect2 = [tuple(map(operator.add, a, center)) for a in rect2]

    draw.rectangle(rect, fill=color)
    draw.rectangle(rect2, fill=color)


# This draws for triangle, square, pentagon, hexagon, heptagon, octagon
def _nsides(draw, color, size, center, n: int):
    a = 2 * math.pi / n
    pts = []
    for s in range(n):
        y, x = math.sin(s * a), math.cos(s * a)
        pts.append((x * size / 2 + center[0], y * size / 2 + center[1]))
    draw.polygon(pts, fill=color)


SHAPE_TO_MAKER = {
    "circle": circle,
    "semicircle": semicircle,
    "quarter_circle": quarter_circle,
    "triangle": triangle,
    "square": square,
    "rectangle": rectangle,
    "trapezoid": trapezoid,
    "pentagon": pentagon,
    "hexagon": hexagon,
    "octagon": octagon,
    "star": star,
    "cross": cross,
}
