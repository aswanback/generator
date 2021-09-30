from math import tan, radians
import cv2
import numpy as np
from PIL import Image


def rotatexyz(image: Image.Image, x: float, y: float, z: float) -> Image.Image:  # All angles in degrees
    """
    img: PIL Image
    x: x axis rotation (perspective)
    y: y axis rotation (perspective)
    z: z axis rotation (euclidean)
    return: PIL Image
    """

    # easy z rotation
    image = image.rotate(z, fillcolor=(0, 0, 0), expand=True)

    # convert to openCV image
    open_cv_image = np.array(image)
    image = open_cv_image[:, :, ::-1].copy()

    # this is the amount that the image will be stretched by
    shape_height, shape_width, _ = image.shape
    delta_x = int(tan(radians(abs(x))) * shape_width)
    delta_y = int(tan(radians(abs(y))) * shape_height)

    # pad the image so it wont ever get cut off
    image = cv2.copyMakeBorder(image, delta_y, delta_y, delta_x, delta_x, cv2.BORDER_CONSTANT)
    height, width, chan = image.shape

    # corners of the shape within padding
    shape_corners = np.float32([
        (delta_x, delta_y),
        (width - delta_x, delta_y),
        (delta_x, height - delta_y),
        (width - delta_x, height - delta_y),
    ])

    # set up what size will stretch
    dx_p = delta_x if x > 0 else 0
    dx_n = delta_x if x < 0 else 0
    dy_p = delta_y if y > 0 else 0
    dy_n = delta_y if y < 0 else 0

    # transform matrix for x and y
    t = np.float32([
        (delta_x - dx_n, delta_y - dy_n),
        (width - delta_x + dx_n, delta_y - dy_p),
        (delta_x - dx_p, height - delta_y + dy_n),
        (width - delta_x + dx_p, height - delta_y + dy_p),
    ])

    # get transform matrix and transform
    transformation_x = cv2.getPerspectiveTransform(shape_corners, t)
    image = cv2.warpPerspective(image, transformation_x, (width, height))

    # debug
    # cv2.imshow('perspective transform', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # crop all the blank space that was created
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    image = image[y:y + h, x:x + w]

    # convert back to PIL
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(image)
    return im_pil


if __name__ == '__main__':
    im = Image.open('shapes/cross-blue-n-black-0.png').convert('RGB')
    im = im.resize((500, 500))
    rot_im = rotatexyz(image=im, x=30, y=20, z=20)
    rot_im.save('test.jpeg')
