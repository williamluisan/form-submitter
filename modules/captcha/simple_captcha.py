import os
from PIL import Image, ImageFilter, ImageOps
import pytesseract
import sys

import numpy as np
from scipy.ndimage import binary_dilation

from modules.captcha.captcha import Captcha
from modules.image.image_file import ImageFile
from modules.image.image_processor import ImageProcessor
from modules.image.image_processor_pytesseract import ImageProcessorPytesseract
from modules.image.image_processor_eocr import ImageProcessorEOCR

class SimpleCaptcha(Captcha):
    def read(self):
        """
        Open downloaded catpcha image
        """
        captcha_img_file = ImageFile('').get_downloaded_image()
        captcha_img_filename = ImageFile(captcha_img_file).get_file_name()
    
        """
        Process to grayscale and its post-processing
        """
        image_raw = ImageFile(captcha_img_file)
        image_gray = ImageProcessor(image_raw.open()).to_grayscale()
        threshold = int(os.getenv('BINARY_IMAGE_THRESHOLD'))
        binary_image = image_gray.point(lambda x: 0 if x < threshold else 255, '1')
        filtered_image = binary_image.filter(ImageFilter.MedianFilter(size=1))

        # save grayscale image
        image_to_save = filtered_image
        image_processor = ImageProcessor(image_to_save)
        image_gray_saved = image_processor.save('gray_' + captcha_img_filename)

        """
        With PyTesseract
        """
        # image_to_read = filtered_image
        # pyTesseractResult = self.__read_with_pytesseract(image_to_read)

        """
        With EasyOCR
        """
        image_to_read = image_gray_saved
        print(f"EasyOCR:")
        easyOCRResult = self.__read_with_easyocr(image_to_read)

        # post string processing after captcha reading
        result = easyOCRResult
        for i in range(len(result)):
            result[i] = result[i].strip().replace(" ", "")

        return result
        
    
    def __read_with_pytesseract(self, image: Image):
        return ImageProcessorPytesseract(image).read()
    
    def __read_with_easyocr(self, image_path: str):
        return ImageProcessorEOCR().read(image_path)