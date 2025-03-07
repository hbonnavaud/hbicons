from PIL import Image
import os
import shutil

# Define target sizes and folders
TARGET_SIZES = {
    '256x256': (256, 256),
    '256x256@2x': (512, 512),
    '128x128': (128, 128),
    '128x128@2x': (256, 256),
    '48x48': (48, 48),
    '48x48@2x': (96, 96),
    '32x32': (32, 32),
    '32x32@2x': (64, 64),
    '24x24': (24, 24),
    '24x24@2x': (48, 48),
    '22x22': (22, 22),
    '22x22@2x': (44, 44),
    '16x16': (16, 16),
    '16x16@2x': (32, 32)
}

def verify_and_copy_icon(icon_path, new_name, target_dir):
    # Check if file exists
    if not os.path.isfile(icon_path):
        print(f"Icon not found: {icon_path}")
        return

    # Open the image
    try:
        img = Image.open(icon_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Verify the size
    if img.size != (512, 512):
        print(f"Invalid image size: {img.size}, expected (512, 512)")
        return

    # Resize and save the image to each target folder
    for folder, size in TARGET_SIZES.items():
        folder_path = os.path.join(target_dir, folder, 'places')
        os.makedirs(folder_path, exist_ok=True)
        resized_img = img.resize(size, Image.ANTIALIAS)
        output_path = os.path.join(folder_path, new_name)
        resized_img.save(output_path, format='PNG')
        print(f"Saved {output_path}")

    print("Icon processed successfully.")

if __name__ == "__main__":
    icon_path = input("Enter the icon path: ")
    new_name = input("Enter the new icon name (with .png extension): ")
    target_dir = "icons/hbicons"  # Base directory to add icons

    verify_and_copy_icon(icon_path, new_name, target_dir)