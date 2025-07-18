from faker import Faker
import time
import os
import pprint
import requests
from bs4 import BeautifulSoup

from modules.captcha.simple_captcha import SimpleCaptcha
from modules.form.faker_provider import FakerProvider
from modules.image.image_file import ImageFile

class Submitter:
    def submit(self):
        TARGET_URL = os.getenv("TARGET_URL")
        SUBMIT_DELAY_TIME = int(os.getenv("SUBMIT_DELAY_TIME"))
        
        print(f"Form submitting attempt start for url: {TARGET_URL}\n")

        session = requests.Session()
        session.headers.update({
            'User-Agent': os.getenv("USER_AGENT_MOCK"), # mocking user agent as mozilla
        })
        res = session.get(TARGET_URL)
        bs4 = BeautifulSoup(res.text, 'html.parser')
        counter = 1

        """
        Form handling
        """
        form = bs4.find('form', {'id': 'self_student_register_from'})
        post_url = form.get('action')
        form_inputs = form.find_all(['input', 'select'], attrs={'name': True})

        """
        Generate payload
        """
        payload = self.generate_payload(form_inputs)

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
            
            time.sleep(SUBMIT_DELAY_TIME) # every 3 seconds
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
                time.sleep(SUBMIT_DELAY_TIME)
                self.submit() # re-call self

        print("No successful attempt.\n")
        time.sleep(SUBMIT_DELAY_TIME)
        print("Re-attempting submit new form...\n")
        time.sleep(SUBMIT_DELAY_TIME)
        self.submit() # re-call self

    def read_simple_captcha(self):
        simple_captcha = SimpleCaptcha()
        return simple_captcha.read()
    
    def generate_payload(self, form_html_str: str):
        """
        To generate appropriate payload to pass
        
        Args:
            form_html_str (str): The raw HTML string input form
        """
        fake = Faker()
        fake.add_provider(FakerProvider)

        payload = {}
        for v_form_inputs in form_html_str:
            element = v_form_inputs.name
            name_attr_val = v_form_inputs.get('name')
            value = v_form_inputs.get('value')
            
            payload[name_attr_val] = 'x' # default

            # CSRF tokens
            if name_attr_val in ['u_token']:
                payload[name_attr_val] = value

            # important form data that is exists in name_attr_val value
            if name_attr_val in ['course_id', 'course_type', 'course_schedule_id']:
                payload[name_attr_val] = value

            # specific case
            if name_attr_val == 'student_type':
                payload[name_attr_val] = 'I'
            if name_attr_val == 'id_type':
                payload[name_attr_val] = 'NRIC'

            # with faker
            if 'student_name' in name_attr_val:
                payload[name_attr_val] = fake.name()
            if 'email' in name_attr_val:
                payload[name_attr_val] = fake.email()
            if name_attr_val == 'contact_no':
                payload[name_attr_val] = fake.singapore_mobile_number()
            if name_attr_val == 'nric':
                payload[name_attr_val] = fake.singapore_nric()

            # handle select input value
            if element == 'select':
                options = v_form_inputs.find_all('option')
                if options:
                    first_value = options[0].get('value', options[0].text.strip())
                    selected = first_value
                    if first_value == '':
                        second_value = options[1].get('value', options[1].text.strip())
                        selected = second_value
                    payload[name_attr_val] = selected

        return payload