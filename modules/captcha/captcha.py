from abc import ABC, abstractmethod

class Captcha(ABC):
    @abstractmethod
    def read(self):
        pass