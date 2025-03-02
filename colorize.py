import os
import sys
import shutil
from PIL import Image, ImageOps
import numpy as np
import pathlib
import cv2
from tqdm import tqdm


SOURCE_PACKAGE_PATH = pathlib.Path("").parent.absolute() / 'icons' / 'reference_set'
SOURCE_PACKAGE_COLOR = np.array([00, 112, 222])


def color_from_ratio(ratio, hexadecimal=True):
    """
    Return a colour that belongs to a gradiant from red (value=0) to green (value=1).
    @param ratio: value between 0 and 1 that defines result color (0 = red, 1 = green)
    @param hexadecimal: THe colour will be return in hexadecimal if true, in a list of RGB int otherwise.
    """
    low_color = [255, 0, 0]
    high_color = [0, 255, 0]
    if hexadecimal:
        result = "#"
    else:
        result = []
    for index, (low, high) in enumerate(zip(low_color, high_color)):
        difference = high - low
        if hexadecimal:
            final_color = hex(int(low + ratio * difference))[2:]
            result += "0" + final_color if len(final_color) == 1 else final_color
        else:
            final_color = int(low + ratio * difference)
            result.append(final_color)
    return result


def compute_mask(image_array, source_color, hue_threshold=5, sat_threshold=30, val_threshold=30, debug=False):
    """
    Compute a mask of pixels that are close enough to the reference color in HSV space.

    Args:
        image_array (np.ndarray): The input image as an RGBA NumPy array.
        source_color (tuple): The reference RGB color (e.g., (200, 50, 50)).
        hue_threshold (int): Hue distance threshold for mask selection.
        sat_threshold (int): Minimum saturation to exclude near-grayscale pixels.

    Returns:
        np.ndarray: Boolean mask indicating pixels to colorize.
    """

    # Convert the entire image from RGB to HSV
    hsv_image = cv2.cvtColor(image_array[:, :, :3].astype(np.uint8), cv2.COLOR_RGB2HSV)

    # Convert reference color to HSV
    source_hsv = cv2.cvtColor(np.uint8([[source_color]]), cv2.COLOR_RGB2HSV)[0][0]

    # Extract Hue, Saturation, and Value channels
    hue, sat, val = hsv_image[:, :, 0].astype(np.int16), hsv_image[:, :, 1], hsv_image[:, :, 2]

    # Compute hue distance correctly without overflow
    source_hue = int(source_hsv[0])  # Convert to int to avoid uint8 issues
    hue_dist_ = np.abs(source_hue - hue)  # Now works correctly
    hue_dist = np.minimum(hue_dist_, 180 - hue_dist_)  # Correct for circular hue wrap-around

    # Mask: Pixels within hue threshold, sufficiently saturated, and not too dark
    mask = (hue_dist <= hue_threshold) & (sat > sat_threshold) & (val > val_threshold)
    return mask


def colorize_filter(image_path, source_color, destination_color, hue_threshold=5, sat_threshold=30, val_threshold=10, colorize_full=False):
    """
    Colorizes only pixels close to the source color.

    Args:
        image_path (str): Path to the image file.
        source_color (tuple): Reference RGB color to replace.
        destination_color (str): Color to apply (e.g., "blue").
        hue_threshold (int): Threshold for hue difference.
        sat_threshold (int): Min saturation to exclude grayscale pixels.
    """
    img = Image.open(image_path).convert("RGBA")
    img_array = np.array(img)

    # Compute optimized mask
    if colorize_full:
        mask = np.ones((img_array.shape[0], img_array.shape[1]), dtype=bool)  # Default to full mask
    else:

        mask = compute_mask(img_array, source_color, hue_threshold, sat_threshold,
                            debug=(image_path.name == "folder.png") & (image_path.parent.parent.name == "16x16"))

    # Convert RGB to grayscale for colorization
    grayscale = np.dot(img_array[:, :, :3], [0.2989, 0.587, 0.114]).astype(np.uint8)

    # Convert to PIL grayscale image
    grayscale_img = Image.fromarray(grayscale, mode="L")

    # Apply color tint to the masked pixels
    colorized = ImageOps.colorize(grayscale_img, black=destination_color, white="white")
    colorized_array = np.array(colorized)

    # Apply mask: Update only masked pixels while preserving alpha
    img_array[mask] = np.hstack((colorized_array[mask], img_array[mask, 3, None]))

    # Convert back to image and save
    result_img = Image.fromarray(img_array, mode="RGBA")
    result_img.save(image_path)

def create_new_color(new_color, new_color_name, full=False):
    if not isinstance(new_color, tuple):
        if not isinstance(new_color, str):
            raise ValueError("new_color must be of type 'string' with hexadecimal format or rgb tuple, not ", type(new_color),
                             ".", sep="")
        else:
            if new_color.startswith("#"):
                new_color = new_color[1:]
            if len(new_color) != 6:
                raise ValueError("new_color must be of type 'string' with hexadecimal format or rgb tuple. "
                                 "Cannot read a string with ", len(new_color), " characters as an hexadecimal color.",
                                 sep="")
            new_color = tuple(int(new_color[i:i + 2], 16) for i in (0, 2, 4))  # Convert hex to RGB
    elif len(new_color) != 3:
        raise ValueError("Expected an rgb color in this tuple, got a tuple with a length different than 3.")
    else:
        for i in new_color:
            if not isinstance(i, int):
                raise ValueError("Expected an rgb color in this tuple, got a tuple without all integer values.")

    # Create the new directory
    current_directory = pathlib.Path(__file__).parent.absolute()
    new_color_path = current_directory / "icons" / ("hbicons-" + new_color_name)
    if not SOURCE_PACKAGE_PATH.exists():
        print("ERROR: can't find the reference icons set directory, ", SOURCE_PACKAGE_PATH,
              ". It is necessary to create a new one.", sep="")
        sys.exit(0)

    if new_color_path.exists():
        shutil.rmtree(new_color_path)
    try:
        shutil.copytree(SOURCE_PACKAGE_PATH, new_color_path)
        print("Directory ", new_color_path, " has been instantiated as a copy of ", SOURCE_PACKAGE_PATH, ".",
              sep="")

        with open(str(new_color_path / "index_to_modify.theme"), "rt") as fin:
            with open(str(new_color_path / "index.theme"), "wt") as fout:
                for line in fin:
                    fout.write(line.replace('colorname', "hbicons-" + new_color_name))
        os.remove(str(new_color_path / "index_to_modify.theme"))
    except FileExistsError:
        print("Error: The destination directory", new_color_path, "already exists.")
    except Exception as e:
        print("An error occurred:", e)

    for image_path in tqdm(new_color_path.rglob("*.png")):
        colorize_filter(image_path, SOURCE_PACKAGE_COLOR, new_color, hue_threshold=30, sat_threshold=0,
                        val_threshold=0, colorize_full=full)
