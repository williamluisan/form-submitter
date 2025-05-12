import requests
from bs4 import BeautifulSoup

from modules.captcha.simple_captcha import SimpleCaptcha
from modules.image.image_file import ImageFile

class Submitter:
    def submit(self):
        target_url = "https://courses.hmi-ihs.com/uat/courses/register/VWJyU2t5VjViNVlnL2xWQUlPWWwwdz09/RUdhWDY3NTBDQmN5NWx0cjFnV1A5UT09"
        res = requests.get(target_url)
        bs4 = BeautifulSoup(res.text, 'html.parser')
        counter = 1

        """
        Captcha handling
        """
        # download captcha image
        captcha_img_path = ''
        captcha_img_elem = bs4.find(id="image_captcha").find('img')
        if captcha_img_elem:
            captcha_img_url = captcha_img_elem['src']
            captcha_image = ImageFile(captcha_img_url).download(counter)
            if captcha_image['status'] is False:
                print(captcha_image['message'])
                return
            else:
                captcha_img_path = captcha_image['path']
            
        # process captcha image to text
        simple_captcha_text = SimpleCaptcha(captcha_img_path).read()

        return "Test submit"

    def read_simple_captcha(self):
        simple_captcha = SimpleCaptcha()
        return simple_captcha.read()