from faker import Faker
from faker.providers import BaseProvider

import random

class FakerProvider(BaseProvider):
    def singapore_mobile_number(self) -> str:
        return f"{random.choice(['8', '9'])}{random.randint(1000000, 9999999)}"
    
    def singapore_nric(self, prefix=None) -> str:
        # choose valid prefix if not specified
        prefix = prefix or random.choice(['S', 'T', 'F', 'G'])
        digits = [random.randint(0, 9) for _ in range(7)]
        
        # weight factors for checksum
        weights = [2, 7, 6, 5, 4, 3, 2]
        weighted_sum = sum(d * w for d, w in zip(digits, weights))

        # adjust for T and G prefixes
        if prefix in ['T', 'G']:
            weighted_sum += 4

        # checksum lookup
        if prefix in ['S', 'T']:
            checksum_letters = ['J','Z','I','H','G','F','E','D','C','B','A']
        else:
            checksum_letters = ['X','W','U','T','R','Q','P','N','M','L','K']

        checksum_index = weighted_sum % 11
        checksum = checksum_letters[checksum_index]

        return f"{prefix}{''.join(str(d) for d in digits)}{checksum}"