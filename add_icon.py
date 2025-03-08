#!/home/hedwin/computing/home_venv/bin/python
import pathlib

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
    '16x16@2x': (32, 32),
    '16x16': (16, 16)
}


def list_download_files():
    home_dir = os.path.expanduser("~")
    download_dir = os.path.join(home_dir, "Téléchargements")

    if not os.path.isdir(download_dir):
        print("Download directory not found.")
        return []

    files = os.listdir(download_dir)
    files = [f for f in files if os.path.isfile(os.path.join(download_dir, f))]

    for idx, file in enumerate(files, 1):
        print(f"{idx} - {file}")

    return files, download_dir


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
        folder_path = os.path.join(target_dir, folder, 'apps')
        os.makedirs(folder_path, exist_ok=True)
        output_path = os.path.join(folder_path, new_name)

        # Remove existing file if it exists
        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"Removed existing icon: {output_path}")

        resized_img = img.resize(size, Image.Resampling.LANCZOS)
        resized_img.save(output_path, format='PNG')
        print(f"Saved {output_path}")

    print("Icon processed successfully.")


if __name__ == "__main__":
    files, download_dir = list_download_files()
    if not files:
        exit()

    try:
        choice = int(input("Select a file number: "))
        if choice < 1 or choice > len(files):
            raise ValueError
    except ValueError:
        print("Invalid choice.")
        exit()

    icon_path = os.path.join(download_dir, files[choice - 1])
    new_name = input("Enter the new icon name: ")
    if not '.' in new_name:
        new_name += ".png"
    elif len(new_name.split(".")) > 2:
        raise ValueError('Cannot manage "." in file names.')
    elif new_name.split(".")[1] != "png":
        raise ValueError('Only ".png" files are supported.')
    target_dir = os.path.expanduser("~") + "/.local/share/icons/hbicons"
    # target_dir = "/usr/share/icons/hbicons"  # Base directory to add icons
    # target_dir = "icons/hbicons"  # Base directory to add icons

    verify_and_copy_icon(icon_path, new_name, target_dir)