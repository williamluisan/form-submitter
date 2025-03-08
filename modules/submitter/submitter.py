from modules.captcha.simple_captcha import SimpleCaptcha

class Submitter:
    def submit(self):
        return "Test submit"

    def read_simple_captcha(self):
        simple_captcha = SimpleCaptcha()
        return simple_captcha.read()