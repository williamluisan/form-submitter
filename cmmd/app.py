import sys
import os
from dotenv import load_dotenv

from modules.form.submitter import Submitter
from modules.form.submitter_playwright import SubmitterPlaywright

load_dotenv(dotenv_path='config/.env')

def main():
    """
    Normal submitter
    """
    submitter = Submitter()

    """
    Playwright submitter
    """
    # submitter = SubmitterPlaywright()

    submitter.submit()

if __name__ == "__main__":
    main()