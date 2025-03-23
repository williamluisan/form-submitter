import os
from PIL import Image, ImageFilter, ImageOps
import pytesseract

from modules.captcha.captcha import Captcha
from modules.image.image_file import ImageFile
from modules.image.image_processor import ImageProcessor

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
        
        threshold = 180
        binary_image = image_gray.point(lambda x: 0 if x < threshold else 255, '1')
        binary_image = binary_image.filter(ImageFilter.MedianFilter(size=1))
        processed_text = pytesseract.image_to_string(binary_image, config='--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        print(processed_text)

        ## dummy (open image)
        image_processor = ImageProcessor(binary_image)
        image_gray_saved = image_processor.save('gray_' + captcha_img_filename)
        # image_file = ImageFile(image_gray_saved)
        # image_file.show_with_explorer()

        return

        ## use spearated image processing class
        ## try .. catch
        # image = Image.open("./public/images/simple_captcha_sample.jpg")
        # image_saved_path = "./tmp/image1.jpg"

        # windows_unc_path = r'\\wsl.localhost\Ubuntu-20.04\home\lunba\Project\form-submitter\tmp\image1.jpg'

        # try:
        #     image.save(image_saved_path)
        # except Exception as e:
        #     print(e)

        # os.system(f'explorer.exe "{windows_unc_path}"')
        
        # image_gray = image.convert('L')
        ## WSL doesnt have GUI, try any way to show the image
        # image.show()
        
        # threshold = 150
        # binary_image = image_gray.point(lambda x: 0 if x < threshold else 255, '1')

        # processed_text = pytesseract.image_to_string(binary_image, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        # print(processed_text)

        # binary_image = ImageOps.invert(binary_image.convert('L'))
        # return "read simple captcha"