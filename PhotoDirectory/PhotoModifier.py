import PIL
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

import PhotoDirectory.Filters as image_filters

import numpy as np


# reads image from path
def read_image(path):
    try:
        image = PIL.Image.open(path)
        return image
    except Exception as e:
        print(e)


# returns image resolution

def get_image_res(image):
    return image.size


# resize image with given height and width (doesn't crop)
def resize_image(image, height, width):
    # remember that image.resize takes in a tuple as input
    resized_image = image.resize((height, width))
    return resized_image


# rotate image counter clockwise with angle
def rotate_image(image, angle):
    return image.rotate(angle)


def flip_image_horizontally(image):
    return image.transpose(PIL.Image.FLIP_LEFT_RIGHT)


def flip_image_vertically(image):
    return image.transpose(PIL.Image.FLIP_TOP_BOTTOM)


# blurs more based on radius
def blur(image, radius):
    return image.filter(ImageFilter.GaussianBlur(radius))


def filter_photo(image, name):
    return image_filters.color_filtered(image, name)


def brighten(image, factor):
    brightener = ImageEnhance.Brightness(image)
    return brightener.enhance(factor)


def contrast(image, factor):
    contraster = ImageEnhance.Contrast(image)
    return contraster.enhance(factor)


def sharpen(image, factor):
    sharpener = ImageEnhance.Sharpness(image)
    return sharpener.enhance(factor)
