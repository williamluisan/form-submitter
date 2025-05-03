from PIL import Image

import pytesseract

from modules.image.image_proc import ImageProc

class ImageProcessorPytesseract(ImageProc):
    config = '--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, image: Image):
        self.image = image
        
    def read(self):
        return pytesseract.image_to_string(self.image, config = self.config)

    def save():
        return

    def to_grayscale():
        return
    
    def more_bolder():
        return