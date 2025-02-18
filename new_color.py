import sys
import argparse
from pathlib import Path
import shutil
from PIL import Image
import numpy as np


def parse_options():
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Require python3.")
        print("Usage: ./new_color [OPTIONS]")
        print("\nOptions:")
        print("  -n, --name   Specify the new template name.")
        print("  -c, --color  Specify the new color (hexadecimal).")
        print("  -h, --help   Show this help message and exit.")
        sys.exit(0)  # Exit after printing help message

    parser = argparse.ArgumentParser(description="Create a new icon set from a given color.")

    parser.add_argument("-n", "--name", type=str, help="Specify the new template name.")
    parser.add_argument("-c", "--color", type=str, help="Specify the new color.")

    args = parser.parse_args()

    result = {
        "name": args.name if args.name else input("  > Select the new color name: "),
        "color": args.color if args.color else input("  > Select the new color in hexadecimal format (# optional): ")
    }

    for forbidden_character in [".", "/"]:
        if forbidden_character in result["name"]:
            print("ERROR: the color name can't contain '%s'" % forbidden_character)
            sys.exit(0)

    if result["color"].startswith("#"):
        result["color"] = result["color"][1:]
    if len(result["color"]) != 6:
        print("ERROR: The color should be in the form RRGGBB (with or without '#'. There is not 6 color character here.")
        sys.exit(0)
    for c in result["color"]:
        if c not in "0123456789abcdefABCDEF":
            print("ERROR: The color name can't contain '%s'" % c)
            sys.exit(0)

    return result


if __name__ == "__main__":
    print()
    print()
    print(" _     _     _                     ")
    print("| |__ | |__ (_) ___ ___  _ __  ___ ")
    print("| '_ \\| '_ \\| |/ __/ _ \\| '_ \\/ __|")
    print("| | | | |_) | | (_| (_) | | | \\__ \\")
    print("|_| |_|_.__/|_|\\___\\___/|_| |_|___/")
    print()
    print()
    print("  === CREATING A NEW HBICON COLOR ===")
    print()
    options = parse_options()

    # Create the new directory
    current_directory = Path(__file__).parent.absolute()
    reference_icon_set_path = current_directory / "icons" / "hbicons-red"
    new_color_path = current_directory / "icons" / ("hbicons-" + options["name"])
    if not reference_icon_set_path.exists():
        print("ERROR: can't find the reference icons set directory, ", reference_icon_set_path,
              ". It is necessary to create a new one.", sep="")
        sys.exit(0)

    if new_color_path.exists():
        print("Error: The directory", new_color_path, "already exists.")
    else:
        try:
            shutil.copytree(reference_icon_set_path, new_color_path)
            print("Directory ", new_color_path, " has been instantiated as a copy of ", reference_icon_set_path, ".",
                  sep="")
        except FileExistsError:
            print("Error: The destination directory", new_color_path, "already exists.")
        except Exception as e:
            print("An error occurred:", e)

    # Get the current color of the copied directory
    reference_icon_path = new_color_path / "256x256" / "emblems" / "emblem-symbolic-link.png"
    image = Image.open(reference_icon_path)         # Load the image
    current_pixel_color = image.getpixel((100, 100))        # Get the color of the pixel at coordinates (x, y)

    # Iterate recursively through icons inside 'new_color_path'
    for icon_path in new_color_path.rglob("*.png"):
        image = Image.open(icon_path).convert("RGBA")
        pixels = np.array(image)  # Convert image to a NumPy array

        # Extract RGBA channels
        red, green, blue, alpha = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2], pixels[:, :, 3]

        # Calculate Euclidean distance from the reference color
        distance = np.sqrt((red - current_pixel_color[0]) ** 2 +
                           (green - current_pixel_color[1]) ** 2 +
                           (blue - current_pixel_color[2]) ** 2)

        # Identify pixels close to the reference color (using a threshold)
        threshold = 50  # Adjust threshold as needed
        mask = distance < threshold

        # Gather statistics on identified pixels
        selected_pixels = pixels[:, :, :3][mask]
        if selected_pixels.size > 0:
            mean_color = np.mean(selected_pixels, axis=0)
            min_color = np.min(selected_pixels, axis=0)
            max_color = np.max(selected_pixels, axis=0)
            std_color = np.std(selected_pixels, axis=0)
            median_color = np.median(selected_pixels, axis=0)
            print(
                f"{icon_path}: Mean={mean_color}, Min={min_color}, Max={max_color}, Std={std_color}, Median={median_color}")

    # Iterate again to colorize the previously identified pixels with 'options["color"]'
    new_color = tuple(int(options["color"][i:i + 2], 16) for i in (0, 2, 4))  # Convert hex to RGB

    for icon_path in new_color_path.rglob("*.png"):
        image = Image.open(icon_path).convert("RGBA")
        pixels = np.array(image)

        # Extract RGBA channels
        red, green, blue, alpha = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2], pixels[:, :, 3]

        # Calculate Euclidean distance from the reference color
        distance = np.sqrt((red - current_pixel_color[0]) ** 2 +
                           (green - current_pixel_color[1]) ** 2 +
                           (blue - current_pixel_color[2]) ** 2)

        # Apply color replacement only to matching pixels
        mask = distance < threshold
        pixels[:, :, 0][mask] = new_color[0]
        pixels[:, :, 1][mask] = new_color[1]
        pixels[:, :, 2][mask] = new_color[2]

        # Save the modified image
        new_image = Image.fromarray(pixels, "RGBA")
        new_image.save(icon_path)
