import sys
import os
from dotenv import load_dotenv

from modules.form.submitter import Submitter
from modules.form.submitter2 import Submitter2

load_dotenv(dotenv_path='config/.env')

def main():
    # submitter = Submitter()
    submitter = Submitter2()

    submitter.submit()

if __name__ == "__main__":
    main()