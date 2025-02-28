#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

import requests
import json
import os
from urllib.parse import urljoin

class ApiClient:
    def __init__(self, base_url="https://reqres.in/api/", timeout=10):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = timeout

    def get(self, endpoint, params=None):
        url = urljoin(self.base_url, endpoint)
        response = self.session.get(url, params=params, timeout=self.timeout)
        return response

    def post(self, endpoint, data):
        url = urljoin(self.base_url, endpoint)
        response = self.session.post(url, json=data)
        return response

    def put(self, endpoint, data):
        url = urljoin(self.base_url, endpoint)
        response = self.session.put(url, json=data)
        return response

    def patch(self, endpoint, data):
        url = urljoin(self.base_url, endpoint)
        response = self.session.patch(url, json=data)
        return response

    def delete(self, endpoint):
        url = urljoin(self.base_url, endpoint)
        response = self.session.delete(url)
        return response

    def load_test_responces_data(self, filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'test_data', 'responses', filename)
        with open(file_path, 'r') as file:
            return json.load(file)

    def load_test_requests_data(self, filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'test_data', filename)
        with open(file_path, 'r') as file:
            return json.load(file)