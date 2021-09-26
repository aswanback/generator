import math
import operator
import random
import colorsys
import cv2
import numpy as np
from PIL import Image

# Enumeration of possible characteristics
Shape = ['CIRCLE','SEMICIRCLE','QUARTERCIRCLE','TRIANGLE','SQUARE','RECTANGLE','TRAPEZOID','PENTAGON','HEXAGON','HEPTAGON','OCTAGON','STAR','CROSS']
Color = ['WHITE','BLACK','GRAY','RED','BLUE','GREEN','YELLOW','PURPLE','BROWN','ORANGE ']
Orientation = ['N','NE','E','SE','S','SW','W','NW']
Alphanumeric = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

# Gets the RGB color of the shape or letter based on color number
def getRandomRGBA(color_num:int):
    # Color = ['WHITE', 'BLACK', 'GRAY', 'RED', 'BLUE', 'GREEN', 'YELLOW', 'PURPLE', 'BROWN', 'ORANGE ']
    # TODO: color ranges
    hue_range = [(0,360),(0,360),(0,360),(-20,20),(150,260),(70,150),(40,70),(260,340),(20,40),(20,40)]
    std_sat = (40,100)
    sat_range = [(0,10),(0,10),(0,10),std_sat,std_sat,std_sat,std_sat,std_sat,(30,60),(60,100)]
    std_light = (40,80)
    light_range = [(80,100),(0,10),(10,30),std_light,std_light,std_light,std_light,std_light,(40,60),(60,80)]

    hue_low,hue_high = hue_range[color_num]
    sat_low,sat_high = sat_range[color_num]
    light_low,light_high = light_range[color_num]

    hue = random.randint(hue_low,hue_high)
    saturation = random.randint(sat_low,sat_high)
    lightness = random.randint(light_low,light_high)

    rgb = colorsys.hls_to_rgb(hue/360,lightness/100,saturation/100)
    rgb = [int(i*255) for i in rgb]
    rgb.append(255) # add alpha
    return tuple(rgb)

# Paste images methods
def pasteImgsCV2(bkgd_file,shape_files,locations,outfilename):
    bkgd = cv2.imread(bkgd_file)

    for i in range(len(shape_files)):
        sh = cv2.imread(shape_files[i])
        mask = np.ones(sh.shape,dtype=sh.dtype)*255
        bkgd = cv2.seamlessClone(sh,bkgd,mask,locations[i],cv2.NORMAL_CLONE)

    cv2.imwrite(outfilename, bkgd)

def pasteImgsPIL(bkgd_file,shape_files,locations,outfilename):
    bkgd = Image.open(bkgd_file,'r')
    for i in range(len(shape_files)):
        sh = Image.open(shape_files[i])
        sh = sh.rotate(random.randint(0,360),fillcolor=(0,0,0,0))
        bkgd.paste(sh,locations[i],sh)
    bkgd.save(outfilename)


# Helpers for drawing individual shapes
def circle(draw, color, size, center):
    draw.ellipse((center[0] - size/2, center[1] - size/2, center[0] + size/2, center[1] + size/2), fill=color)
def semicircle(draw, color, size, center):
    size = size/2
    draw.pieslice((center[0] - size, center[1] - size - size / 2, center[0] + size, center[1] + size - size / 2),
                  start=0, end=180, fill=color)
def quartercircle(draw, color, size, center):
    size = size/1.15
    draw.pieslice((center[0] - size - size *4/3/3.14159, center[1] - size - size*4/3/3.14159, center[0] + size - size*4/3/3.14159,
                   center[1] + size - size *4/3/3.14159), start=0, end=90, fill=color)
def triangle(draw, color, size, center):
    _nsides(draw, color, size, center, 3) #equilateral
    # Equilateral
    # w = size*2
    # h = w*math.sqrt(3)/2
    # # Right Triangle 1-1-sqrt(2)
    # w = size
    # h = w / 2
    # centroidy = h/6
    # draw.polygon(((center[0], center[1] + h / 2+centroidy), (center[0] - w / 2, center[1] - h / 2+centroidy),(center[0] + w / 2, center[1] - h / 2+centroidy)), fill=color)
def square(draw, color, size, center):
    _nsides(draw, color, size, center, 4)
    # draw.rectangle((center[0] - size / 2, center[1] - size / 2, center[0] + size / 2, center[1] + size / 2),fill=color)
def rectangle(draw, color, size, center):
    aspect = 0.8 #TODO: make rectangle aspect ratio random?
    draw.rectangle(
        (center[0] - size / 2, center[1] - size / 2 * aspect, center[0] + size / 2, center[1] + size / 2 * aspect),
        fill=color)
def trapezoid(draw, color, size, center):
    d = size/5  # offset width
    hh = size/3 # half height
    hw = size/2 # half width
    draw.polygon(((center[0]-hw,center[1]+hh),(center[0]-hw+d,center[1]-hh),(center[0]+hw,center[1]-hh),(center[0]+hw-d,center[1]+hh)),fill=color)
def pentagon(draw, color, size, center):
    _nsides(draw, color, size, center, 5)
def hexagon(draw, color, size, center):
    _nsides(draw, color, size, center, 6)
def heptagon(draw, color, size, center):
    _nsides(draw, color, size, center, 7)
def octagon(draw, color, size, center):
    _nsides(draw, color, size, center, 8)
def star(draw, color, size, center):
    h = size / 5.9 # why? dont ask
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
        w = size/2
        h = w/3
        rect = ((-w, h), (w, -h))

        c, s = math.cos(math.pi / 2), math.sin(math.pi / 2)
        rect2 = tuple([(c * x - s * y, s * x + c * y) for (x, y) in rect])

        rect = [tuple(map(operator.add, a, center)) for a in rect]
        rect2 = [tuple(map(operator.add, a, center)) for a in rect2]

        draw.rectangle(rect, fill=color)
        draw.rectangle(rect2, fill=color)

# This draws for triangle, square, pentagon, hexagon, heptagon, octagon
def _nsides(draw, color, size, center, n:int):
    a = 2 * math.pi / n
    pts = []
    for s in range(n):
        y, x = math.sin(s * a), math.cos(s * a)
        pts.append((x * size/2 + center[0], y * size/2 + center[1]))
    draw.polygon(pts, fill=color)
