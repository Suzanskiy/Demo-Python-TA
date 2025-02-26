#  © 2025 Serhii Suzanskyi 🚀
#  Open-source and awesome! Use it, modify it, share it—just don’t break it. 😉
#  See LICENSE for details.

import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, params=None, headers=None):
        return self.session.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=headers
        )

    def post(self, endpoint, data=None, json=None, headers=None):
        return self.session.post(
            f"{self.base_url}{endpoint}",
            data=data,
            json=json,
            headers=headers
        )