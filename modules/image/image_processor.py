from PIL import Image

SAVE_PATH = './tmp'

class ImageProcessor():
    def __init__(self, image: Image):
        self.image = image

    def to_grayscale(self):
        return self.image.convert('L')
    
    def save(self, filename: str = None):
        image = self.image
        path = f'{SAVE_PATH}/{filename}'
    
        ## TODO:
        # try .. catch ..
        image.save(path)

        return path