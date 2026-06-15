import json
import os
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from faker import Faker

from modules.form.faker_provider import FakerProvider


class Submitter2:
    """
    Submitter for Livewire v3 forms.

    Unlike a plain HTML form, a Livewire v3 component does not POST form-data to
    a form `action`. Instead the browser sends a JSON request to `/livewire/update`
    carrying the component's `wire:snapshot`, a dict of property `updates`, and a
    list of `calls` (the method the submit button triggers, e.g. `save`).
    """

    def submit(self):
        TARGET_URL = os.getenv("TARGET_URL")
        SUBMIT_DELAY_TIME = int(os.getenv("SUBMIT_DELAY_TIME"))
        # the Livewire action the form's submit button invokes (wire:submit="...")
        SUBMIT_METHOD = os.getenv("LIVEWIRE_SUBMIT_METHOD", "save")

        print(f"Livewire form submitting attempt start for url: {TARGET_URL}\n")

        session = requests.Session()
        session.headers.update({
            'User-Agent': os.getenv("USER_AGENT_MOCK"),  # mocking user agent as mozilla
        })

        res = session.get(TARGET_URL)
        bs4 = BeautifulSoup(res.text, 'html.parser')

        """
        Livewire component discovery
        """
        component = bs4.find(attrs={'wire:snapshot': True})
        if component is None:
            print("No Livewire component (wire:snapshot) found on the page.")
            return

        # wire:snapshot is an HTML-encoded JSON string; BeautifulSoup decodes the
        # entities for us, leaving raw JSON text. Livewire expects this exact string
        # echoed back in the request, so keep both the string and a parsed copy.
        snapshot_str = component.get('wire:snapshot')
        try:
            snapshot = json.loads(snapshot_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse wire:snapshot JSON: {e}")
            return
        print(snapshot_str)
        exit()

        """
        CSRF token + update endpoint discovery
        """
        csrf_token = self.extract_csrf_token(bs4)
        if not csrf_token:
            print("Could not locate CSRF token.")
            return

        update_url = urljoin(TARGET_URL, self.extract_update_uri(res.text))

        """
        Generate payload from the component's data properties
        """
        updates = self.generate_payload(snapshot.get('data', {}))

        body = {
            "_token": csrf_token,
            "components": [
                {
                    "snapshot": snapshot_str,
                    "updates": updates,
                    "calls": [
                        {"path": "", "method": SUBMIT_METHOD, "params": []}
                    ],
                }
            ],
        }

        """
        Submitting
        """
        time.sleep(SUBMIT_DELAY_TIME)
        res = session.post(update_url, json=body, headers={
            'X-Livewire': '',
            'X-CSRF-TOKEN': csrf_token,
            'Content-Type': 'application/json',
            'Accept': 'text/html, application/xhtml+xml',
            'Referer': TARGET_URL,
        })

        print(f"\nResponse status: {res.status_code}")
        try:
            data = res.json()
        except json.JSONDecodeError:
            print(res.text)
            return

        # Livewire returns validation errors / effects per component
        effects = data.get('components', [{}])[0].get('effects', {})
        if 'returns' in effects or res.status_code == 200:
            print("Form submitted!")
        print(json.dumps(data, indent=2))

    def extract_csrf_token(self, bs4: BeautifulSoup):
        """
        Resolve the CSRF token Livewire needs for /livewire/update.

        Tries the standard <meta name="csrf-token"> first, then the token Livewire
        embeds in `window.livewireScriptConfig`.
        """
        meta = bs4.find('meta', attrs={'name': 'csrf-token'})
        if meta and meta.get('content'):
            return meta.get('content')

        config = self.extract_livewire_config(str(bs4))
        if config:
            return config.get('csrf')

        return None

    def extract_update_uri(self, html: str):
        """The endpoint Livewire posts to, falling back to the v3 default."""
        config = self.extract_livewire_config(html)
        if config and config.get('uri'):
            return config['uri']
        return '/livewire/update'

    def extract_livewire_config(self, html: str):
        """Parse the `window.livewireScriptConfig = {...}` JSON blob if present."""
        match = re.search(r'livewireScriptConfig\s*=\s*(\{.*?\})\s*;', html, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None

    def generate_payload(self, data: dict):
        """
        Build the `updates` dict from the component's data properties.

        Args:
            data (dict): the `data` object decoded from the wire:snapshot
        """
        fake = Faker()
        fake.add_provider(FakerProvider)

        payload = {}
        for name_attr_val, current_value in data.items():
            # Livewire serializes nested props as [value, metadata]; skip those,
            # we only auto-fill scalar fields.
            if isinstance(current_value, (list, dict)):
                continue

            payload[name_attr_val] = 'x'  # default

            # specific case
            if name_attr_val == 'student_type':
                payload[name_attr_val] = 'I'
            if name_attr_val == 'id_type':
                payload[name_attr_val] = 'NRIC'

            # with faker
            if 'student_name' in name_attr_val or name_attr_val == 'name':
                payload[name_attr_val] = fake.name()
            if 'email' in name_attr_val:
                payload[name_attr_val] = fake.email()
            if name_attr_val == 'contact_no':
                payload[name_attr_val] = fake.singapore_mobile_number()
            if name_attr_val == 'nric':
                payload[name_attr_val] = fake.singapore_nric()

        return payload
