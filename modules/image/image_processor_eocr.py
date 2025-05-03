import easyocr
from itertools import permutations
import sys

from modules.image.image_proc import ImageProc

class ImageProcessorEOCR(ImageProc):
    reader = None

    def __init__(self):
        # specify easyocr language
        self.reader = easyocr.Reader(['en'])
    
    def read(self, image_path) -> list:
        result = self.reader.readtext(image_path)
        text_result_list = []
        for (bbox, text, probability) in result:
            text_result_list.append(text)

        # process with permutation for every possible combination
        combinations_text_result_list = []
        for p in permutations(text_result_list):
            combination = ''.join(p)
            combinations_text_result_list.append(combination)

        return combinations_text_result_list

    def save():
        return

    def to_grayscale():
        return
    
    def more_bolder():
        return