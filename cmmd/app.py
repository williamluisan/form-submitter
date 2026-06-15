import sys
import os
from dotenv import load_dotenv

from modules.form.submitter import Submitter
from modules.form.submitterPlaywright import SubmitterPlaywright

load_dotenv(dotenv_path='config/.env')

def main():
    # submitter = Submitter()
    submitter = SubmitterPlaywright()

    submitter.submit()

if __name__ == "__main__":
    main()