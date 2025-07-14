import os
from abc import ABC, abstractmethod

class ImageProc(ABC):
    SAVE_PATH = os.getenv("GRAYSCALE_PROCESSED_IMAGE_SAVED_PATH")

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