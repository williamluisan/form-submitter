from modules.captcha.captcha import Captcha

class Recaptcha(Captcha):
    def __init__(self, recaptcha_html_elem: str):
        self.recaptcha_html_elem = recaptcha_html_elem

    def read(self) -> None:
        return self.recaptcha_html_elem
    

