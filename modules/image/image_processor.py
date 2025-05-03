from PIL import Image

import numpy as np
from scipy.ndimage import binary_dilation

from modules.image.image_proc import ImageProc

class ImageProcessor(ImageProc):
    def __init__(self, image: Image):
        self.image = image

    def read(self):
        return

    def to_grayscale(self):
        return self.image.convert('L')
    
    def save(self, filename: str = None):
        image = self.image
        path = f'{ImageProc.SAVE_PATH}/{filename}'
    
        ## TODO:
        # try .. catch ..
        image.save(path)

        return path

    """
    To apply dilation to the image
    """
    def more_bolder(self, thickness = 2):
        dilation_matrix_height = thickness
        dilation_matrix_width = thickness

        # Convert binary PIL image to NumPy array
        binary_np = np.array(self.image) == 0  # True for black

        # Apply dilation to bolden black areas
        dilated_np = binary_dilation(binary_np, structure=np.ones((dilation_matrix_height, dilation_matrix_width)))

        # Invert and convert back to uint8
        bolded_np = (~dilated_np * 255).astype(np.uint8)

        # Convert back to PIL Image (mode 'L')
        bolded_image = Image.fromarray(bolded_np, mode='L')

        return bolded_image