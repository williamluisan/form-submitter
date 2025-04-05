from abc import ABC, abstractmethod

class ImageProc(ABC):
    SAVE_PATH = './tmp'

    @abstractmethod
    def to_grayscale(self):
        pass

    @abstractmethod
    def save(self):
        pass