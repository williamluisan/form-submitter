import easyocr

from modules.image.image_proc import ImageProc

class ImageProcessorEOCR(ImageProc):
    reader = None

    def __init__(self):
        # specify easyocr language
        self.reader = easyocr.Reader(['en'])
    
    def read(self, image_path):
        return self.reader.readtext(image_path)

    def to_grayscale():
        return

    def save():
        return