import os
import requests
import subprocess
from PIL import Image
from datetime import datetime

DOWNLOAD_PATH = './public/images' 

class ImageFile():
    def __init__(self, img_path: str):
        self.img_path = img_path
    
    def open(self):
        return Image.open(self.img_path)

    """
    with Requests library
    """
    def download(self, name_id: str = None):
        error_msg_perfix = 'Image download: '
        error_msg = ''

        timestamp = int(datetime.now().timestamp())
        
        filename = timestamp
        if name_id is not None:
            filename = f'{timestamp}_{name_id}'

        img_binary = requests.get(self.img_path).content
        try:
            with open(f'{DOWNLOAD_PATH}/{filename}.jpg', 'wb') as f:
                f.write(img_binary)
        except Exception as e:
            error_msg = f'{error_msg_perfix}{e}'
        
        if error_msg != '':
            return error_msg
        return True

    def get_downloaded_image(self):
        img_path = f'{DOWNLOAD_PATH}/2.jpg'
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