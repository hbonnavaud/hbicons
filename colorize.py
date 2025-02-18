from PIL import Image, ImageEnhance, ImageOps
import os
import pathlib

# Define your custom color
c = "a"

COLORIZE_HEX = "#" + c * 6

# Convert hex to RGB
hex_to_rgb = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
COLORIZE_RGB = hex_to_rgb(COLORIZE_HEX)

# Base directory for icons
ICON_DIR = str(pathlib.Path(__file__).parent.absolute())

# Process all PNG images recursively
def process_images():
    for root, _, files in os.walk(ICON_DIR):
        for file in files:
            if file.endswith(".png"):
                img_path = os.path.join(root, file)
                print(f"Processing: {img_path}")
                
                # Open image with RGBA (includes alpha channel)
                img = Image.open(img_path).convert("RGBA")
                
                # Split the image into its RGBA channels
                r, g, b, a = img.split()
                
                # Convert RGB to grayscale and normalize it
                grayscale = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))
                
                # Normalize grayscale to [0, 255] range to ensure consistency across images
                min_val = min(grayscale.getdata())
                max_val = max(grayscale.getdata())
                normalized = grayscale.point(lambda p: 255 * (p - min_val) / (max_val - min_val) if max_val != min_val else p)
                
                # Apply color tint to the normalized grayscale image
                colorized = ImageOps.colorize(normalized, black="black", white=COLORIZE_RGB)
                
                # Optionally, enhance the contrast to match the lightness of folder-document.png
                enhancer = ImageEnhance.Contrast(colorized)
                colorized = enhancer.enhance(1.2)  # Adjust contrast (1.2 is an example, tweak as needed)
                
                # Merge the colorized image back with the original alpha channel
                img = Image.merge("RGBA", (colorized.split()[0], colorized.split()[1], colorized.split()[2], a))
                
                # Save the colorized image
                img.save(img_path)
                print(f"Saved: {img_path}")

if __name__ == "__main__":
    process_images()
    print("All icons have been colorized!")
