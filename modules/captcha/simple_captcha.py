import os
from PIL import Image, ImageFilter, ImageOps
import pytesseract

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
        Process to grayscale
        """
        image_raw = ImageFile(captcha_img_file)
        image_gray = ImageProcessor(image_raw.open()).to_grayscale()
        
        threshold = 178
        binary_image = image_gray.point(lambda x: 0 if x < threshold else 255, '1')
        binary_image = binary_image.filter(ImageFilter.MedianFilter(size=1))
        
        # save grayscale image
        image_processor = ImageProcessor(binary_image)
        image_gray_saved = image_processor.save('gray_' + captcha_img_filename)
        
        """
        Read using PyTesseract
        """
        pyTesseractResult = ImageProcessorPytesseract(binary_image).read()
        print(f"PyTesseract:")
        print(pyTesseractResult)

        """
        Read using EasyOCR
        """
        easyOCRResult = ImageProcessorEOCR().read(image_gray_saved)
        print(f"EasyOCR:")
        for (bbox, text, prob) in easyOCRResult:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            print(f'Text: {text}, Probability: {prob}')