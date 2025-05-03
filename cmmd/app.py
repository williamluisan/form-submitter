import sys
import os

from modules.submitter.submitter import Submitter

def main():
    submitter = Submitter()
    submitter.read_simple_captcha()

if __name__ == "__main__":
    main()