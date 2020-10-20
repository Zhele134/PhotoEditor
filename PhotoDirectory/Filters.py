import PIL
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np

class Filters:
    color_filters = {
        "Greyscale": "Greyscale",
        "Negative": "Negative",
        "Sepia": "Sepia",
        "Crimson": "Crimson",
        "BlackAndWhite": "BlackAndWhite"
    }
    GREYSCALE, NEGATIVE, SEPIA, CRIMSON, BW = color_filters.keys()

# adapted from https://haru-atari.com/blog/30-write-simple-image-filters-in-python
def convert_to_grayscale(image):
    grayscale = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = grayscale[x, y]
            gray = int(r * 0.2126 + g * 0.7152 + b * 0.0722)
            grayscale[x, y] = (gray, gray, gray)
    return grayscale


# adapted from https://haru-atari.com/blog/30-write-simple-image-filters-in-python
# inverts photo colors
def negative(image):
    negative_img = image.load()
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = negative_img[x,y]
            negative_img[x, y] = (225 - r, 225 - g, 225 - b)
    return negative_img


# method found on https://haru-atari.com/blog/30-write-simple-image-filters-in-python
def sepia(image):
    sepia_copy = image.load()
    # gets each individual pixel
    for x in range(image.width):
        for y in range(image.height):
            # gets rgb values of each pixel
            r, g, b = sepia_copy[x, y]
            # averages each color value to sepia color
            red = int(r * 0.393 + g * 0.769 + b * 0.189)
            green = int(r * 0.349 + g * 0.686 + b * 0.168)
            blue = int(r * 0.272 + g * 0.534 + b * 0.131)
            # replace each pixel color with a sepia value
            sepia_copy[x, y] = (red, green, blue)
    return sepia_copy


# method from https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
def Black_And_White(image):
    # resampling changes number of pixels in picture, so pixelating makes less pixels
    bw_copy = image.load()
    brightness = 1.1
    threshold = 255 / brightness / 2 * 3
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = bw_copy[x, y]
            total = r + g + b
            if total > threshold:
                bw_copy[x, y] = (255, 255, 255)
            else:
                bw_copy[x, y] = (0, 0, 0)
    return bw_copy




def crimson(image):
    red_copy = image.load()
    # gets each individual pixel
    for x in range(image.width):
        for y in range(image.height):
            # gets rgb values of each pixel
            r, g, b = red_copy[x, y]
            # averages each color value to crimson color
            red = int(r * 0.680 + g * 0.720 + b * 0.740)
            green = int(r * 0.387 + g * 0.478 + b * 0.168)
            blue = int(r * 0.5 + g * 0.534 + b * 0.4)
            # replace each pixel color with a crimson value
            red_copy[x, y] = (red, green, blue)
    return red_copy


def color_filtered(img, name):
    img_copy = img.copy()
    if name == Filters.GREYSCALE:
        convert_to_grayscale(img_copy)
    elif name == Filters.NEGATIVE:
        negative(img_copy)
    elif name == Filters.SEPIA:
        sepia(img_copy)
    elif name == Filters.CRIMSON:
        crimson(img_copy)
    elif name == Filters.BW:
        Black_And_White(img_copy)
    else:
        raise ValueError(f"Can't find filter {name}")
    return img_copy
