import sys
import os
from dotenv import load_dotenv

from modules.submitter.submitter import Submitter

load_dotenv(dotenv_path='config/.env')

def main():
    submitter = Submitter()
    submitter.submit()

if __name__ == "__main__":
    main()