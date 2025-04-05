from PIL import Image

from modules.image.image_proc import ImageProc

class ImageProcessor(ImageProc):
    def __init__(self, image: Image):
        self.image = image

    def to_grayscale(self):
        return self.image.convert('L')
    
    def save(self, filename: str = None):
        image = self.image
        path = f'{ImageProc.SAVE_PATH}/{filename}'
    
        ## TODO:
        # try .. catch ..
        image.save(path)

        return path