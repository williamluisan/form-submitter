import os
from PIL import Image
import subprocess

DOWNLOAD_PATH = './public/images' 

class ImageFile():
    def __init__(self, img_path: str):
        self.img_path = img_path
    
    def open(self):
        return Image.open(self.img_path)

    def get_downloaded_image(self):
        img_path = f'{DOWNLOAD_PATH}/simple_captcha_sample3.jpg'
        return img_path

    def get_file_name(self):
        return os.path.basename(self.img_path)

    def show_with_explorer(self):
        # UNC path to access file to WSL
        UNC_PATH = r'\\wsl.localhost\Ubuntu-20.04\home\lunba\Project\form-submitter'
        
        img_path = self.img_path
        img_path_UNC = img_path.lstrip('.').replace('/', '\\')
        img_path_UNC_complete = f'{UNC_PATH}{img_path_UNC}' 

        # open with windows explorer
        subprocess.run(['explorer.exe', img_path_UNC_complete])