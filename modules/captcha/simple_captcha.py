from modules.captcha.captcha import Captcha

class SimpleCaptcha(Captcha):
    def read(self):
        return "read simple captcha"