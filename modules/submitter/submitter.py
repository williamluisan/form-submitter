import time
import pprint
import requests
from bs4 import BeautifulSoup

from modules.captcha.simple_captcha import SimpleCaptcha
from modules.image.image_file import ImageFile

class Submitter:
    def submit(self):
        # target_url = "https://courses.hmi-ihs.com/uat/courses/register/VWJyU2t5VjViNVlnL2xWQUlPWWwwdz09/RUdhWDY3NTBDQmN5NWx0cjFnV1A5UT09"
        target_url = "https://shri.dlideas.com/courses/register/M2NtdVAzREw5QVhQMzRvektsQmxKUT09/RUdhWDY3NTBDQmN5NWx0cjFnV1A5UT09/1"
        res = requests.get(target_url)
        bs4 = BeautifulSoup(res.text, 'html.parser')
        counter = 1

        """
        Form handling
        """
        form = bs4.find('form', {'id': 'self_student_register_from'})
        post_url = form.get('action')
        form_inputs = form.find_all('input', attrs={'name': True})

        """
        Generate payload
        """
        payload = {}
        for v_form_inputs in form_inputs:
            element = v_form_inputs.get('name')
            payload[element] = 'a'
        
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
        if not simple_captcha_text:
            print("No captcha text extracted.")
            return

        """
        Submitting
        """
        attempt_counter = 0
        for v_sct in simple_captcha_text:
            # update captcha payload
            payload['verification_code'] = v_sct
            
            time.sleep(3) # every 3 seconds
            attempt_counter += 1
            res = requests.post(post_url, data=payload)
            if (res.text == "verification_mismatch"):
                print(f'Attempt {attempt_counter}: {res.text} - captcha: {payload['verification_code']}\n')
            else:
                print(f'Attempt {attempt_counter}: {res.text}\n')

        print("Finished!")
        return

    def read_simple_captcha(self):
        simple_captcha = SimpleCaptcha()
        return simple_captcha.read()