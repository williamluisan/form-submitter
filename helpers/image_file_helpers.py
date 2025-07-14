import os
from pathlib import Path

def clear_downloaded_captcha_image(keep: int = 1):
    min_downloaded_img = 10
    ext = ".jpg"
    folder = Path(os.getenv("CAPTCHA_IMAGE_DOWNLOAD_PATH"))

    img_files = [img for img in folder.iterdir() if img.is_file() and img.suffix.lower() == ext]
    total = len(img_files)

    img_files_sorted = sorted(img_files, key=lambda file: int(file.stem))

    if total > min_downloaded_img:
        for file in img_files_sorted[:-keep]:
            file.unlink()
        

def clear_grayscale_processed_captcha_image(keep: int = 1):
    min_processed_img = 10
    ext = ".jpg"
    folder = Path(os.getenv("GRAYSCALE_PROCESSED_IMAGE_SAVED_PATH"))

    img_files = [img for img in folder.iterdir() if img.is_file() and img.suffix.lower() == ext]
    total = len(img_files)

    img_files_sorted = sorted(img_files, key=lambda file: str(file.stem))

    if total > min_processed_img:
        for file in img_files_sorted[:-keep]:
            file.unlink()