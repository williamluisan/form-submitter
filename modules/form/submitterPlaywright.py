from playwright.sync_api import sync_playwright

class SubmitterPlaywright:
    def submit(self):
        with sync_playwright() as p:
            browser = p.firefox.launch(
                headless=False,
            )
            page = browser.new_page()

            page.goto("http://localhost:8093/onboarding/01KS492QFYSGMXPAQGKN24144H")
            page.select_option('select[id="data.title"]', value="Mr.")
            page.fill('input[id="data.first_name"]', "FirstName")
            page.fill('input[id="data.last_name"]', "LastName")
            page.fill('input[id="data.preferred_first_name"]', "PreferredFirstName")
            page.fill('input[id="data.date_of_birth"]', "2000-01-01")
            page.select_option('select[id="data.gender"]', value="Male")
            page.fill('input[id="phone_personal_phone"]', "123123")
            page.fill('input[id="data.personal_email"]', "personalemail@ictechnology.com.au")
            page.fill('input[id="data.company_email"]', "companyemail@ictechnology.com.au")
            page.fill('textarea[id="data.residential_address"]', "ResidentialAddress")
            page.fill('input[id="data.emergency_contact_name"]', "1")
            page.select_option('select[id="data.emergency_contact_relationship"]', value="Son")
            page.fill('input[id="phone_emergency_contact_phone"]', "123123")
            page.fill('input[id="data.tax_file_number"]', "1")
            page.fill('input[id="data.bank_account_name"]', "1")
            page.fill('input[id="data.bank_account_number"]', "1")
            page.fill('input[id="data.bank_bsb"]', "1")

            page.click('button[wire\\:target="save"]')

            input("Press Enter...")