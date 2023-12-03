import requests


class BaseRESTClient:

    def __init__(self, access_token, base_api_url):
        self.access_token = access_token
        self.base_api_url = base_api_url

    def __generate_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def get(self, command_path):
        url = f"{self.base_api_url}{command_path}"
        headers = self.__generate_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
