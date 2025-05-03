from abc import ABC, abstractmethod

class ImageProc(ABC):
    SAVE_PATH = './tmp'

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def to_grayscale(self):
        pass

    @abstractmethod
    def more_bolder(self):
        pass