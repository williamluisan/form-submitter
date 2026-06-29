import os
import time

from playwright.sync_api import sync_playwright
from faker import Faker


class SubmitterPlaywright:
    def submit(self):
        TARGET_URL = os.getenv("TARGET_URL")
        SUBMIT_DELAY_TIME = int(os.getenv("SUBMIT_DELAY_TIME"))

        fake = Faker()

        with sync_playwright() as p:
            browser = p.firefox.launch(
                headless=True,
            )
            page = browser.new_page()

            print(f"Form submitting attempt start for url: {TARGET_URL}")

            attempt = 0
            while True:
                attempt += 1
                first_name = fake.first_name()
                email = fake.email()

                page.goto(TARGET_URL)

                page.select_option('select[id="data.title"]', value="Mr.")
                page.fill('input[id="data.first_name"]', first_name)
                page.fill('input[id="data.last_name"]', fake.last_name())
                page.fill('input[id="data.preferred_first_name"]', first_name)
                page.evaluate("""
                    const el = document.querySelector('input[id="data.date_of_birth"]');
                    el.removeAttribute('readonly');
                    el.value = '2000-01-01';
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                """)
                page.select_option('select[id="data.gender"]', value="Male")
                page.fill('input[id="phone_personal_phone"]', fake.phone_number())
                page.fill('input[id="data.personal_email"]', email)
                page.fill('input[id="data.company_email"]', email)
                page.fill('textarea[id="data.residential_address"]', fake.address())
                page.fill('input[id="data.emergency_contact_name"]', fake.name())
                page.select_option('select[id="data.emergency_contact_relationship"]', value="Family")
                page.fill('input[id="phone_emergency_contact_phone"]', fake.phone_number())
                page.fill('input[id="data.tax_file_number"]', "1")
                page.fill('input[id="data.bank_account_name"]', "1")
                page.fill('input[id="data.bank_account_number"]', "1")
                page.fill('input[id="data.bank_bsb"]', "1")

                page.click('button[wire\\:target="save"]')

                print(f"Submitted form #{attempt}")
                time.sleep(SUBMIT_DELAY_TIME)