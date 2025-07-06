import time
import pprint
import requests
from bs4 import BeautifulSoup

from modules.captcha.simple_captcha import SimpleCaptcha
from modules.image.image_file import ImageFile

class Submitter:
    def submit(self):
        # target_url = "https://courses.hmi-ihs.com/uat/courses/register/VWJyU2t5VjViNVlnL2xWQUlPWWwwdz09/RUdhWDY3NTBDQmN5NWx0cjFnV1A5UT09"
        target_url = "https://shri.dlideas.com/courses/register/WkZoOENqVWNJT3graHBsYUkyWGp2QT09/RUdhWDY3NTBDQmN5NWx0cjFnV1A5UT09/1"
        # target_url = "http://localhost:8081/dl_shri/courses/register/cENuN0FnQ3hXM1kyaVRGWVhCVGEydz09/RUdhWDY3NTBDQmN5NWx0cjFnV1A5UT09/1"
        
        print(f"Form submitting attempt start for url: {target_url}\n")

        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0', # mocking user agent as mozilla
        })
        res = session.get(target_url)
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
            
            # TODO: do with faker
            payload[element] = 'a'

            # TODO: read the value from the view
            if element == 'course_schedule_id':
                payload[element] = 195
            
            # TODO: read the value from the view
            if element == 'course_type':
                payload[element] = 'S'

            # TODO: with faker
            if element == 'email':
                payload[element] = 'johndoe1122@dlideas.com'
        
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
            res = session.post(post_url, data=payload)
            if (res.text == "verification_mismatch"):
                print(f'\nAttempt {attempt_counter}: {res.text} - captcha: {payload['verification_code']}')
            else:
                print(f'\nAttempt {attempt_counter}: {res.text}\n')
                print(payload)
                print("\n")
                print(res.text)
                print("Form submitted!")
                return

        print("No successful attempt.\n")
        time.sleep(3)
        print("Re-attempting submit new form...\n")
        time.sleep(3)
        self.submit() # re-call self function

    def read_simple_captcha(self):
        simple_captcha = SimpleCaptcha()
        return simple_captcha.read()