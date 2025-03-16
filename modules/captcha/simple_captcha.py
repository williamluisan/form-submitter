from PIL import Image
import pytesseract

from modules.captcha.captcha import Captcha

class SimpleCaptcha(Captcha):
    def read(self):
        ## use spearated image processing class
        ## try .. catch
        image = Image.open("./public/images/simple_captcha_sample.jpg")
        image_gray = image.convert('L')
        ## WSL doesnt have GUI, try any way to show the image
        # image.show()
        
        threshold = 150
        binary_image = image_gray.point(lambda x: 0 if x < threshold else 255, '1')

        processed_text = pytesseract.image_to_string(binary_image, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        print(processed_text)

        # return "read simple captcha"