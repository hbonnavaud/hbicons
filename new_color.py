import sys
import argparse
import pathlib
from colorize import create_new_color


SOURCE_PACKAGE_PATH = pathlib.Path("").parent.absolute() / 'icons' / 'hbicons-red'


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
    parser.add_argument("-f", "--full", action="store_true",
                        help="Specify if the icons have to be fully colorized (default: False)")

    args = parser.parse_args()

    result = {
        "name": args.name if args.name else input("  > Select the new color name: "),
        "color": args.color if args.color else input("  > Select the new color in hexadecimal format (# optional): "),
        "full": args.full
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

    create_new_color(new_color=options["color"])
    # Create the new directory
    current_directory = pathlib.Path(__file__).parent.absolute()
    new_color_path = current_directory / "icons" / ("hbicons-" + options["name"])

    # Iterate again to colorize the previously identified pixels with 'options["color"]'
    new_color = tuple(int(options["color"][i:i + 2], 16) for i in (0, 2, 4))  # Convert hex to RGB
    create_new_color(new_color, options["name"], full=options["full"])
