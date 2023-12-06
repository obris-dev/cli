import requests


class BaseRESTClient:

    def __init__(self, access_token, base_api_url):
        self.access_token = access_token
        self.base_api_url = base_api_url

    def __generate_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def __generate_url(self, command_path):
        return f"{self.base_api_url}{command_path}"

    def get(self, command_path, params=None):
        return self.__make_request("get", command_path, params=params)

    def post(self, command_path, data):
        return self.__make_request("post", command_path, json=data)

    def put(self, command_path, data):
        return self.__make_request("put", command_path, json=data)

    def delete(self, command_path):
        return self.__make_request("delete", command_path)

    def __make_request(self, http_method, command_path, json=None, params=None):
        url = self.__generate_url(command_path)
        headers = self.__generate_headers()

        additional_kwargs = {}
        if json is not None:
            additional_kwargs["json"] = json
        elif params is not None:
            additional_kwargs["params"] = params

        method = getattr(requests, http_method)
        response = method(url, headers=headers, **additional_kwargs)
        response.raise_for_status()

        if response.status_code == 204:
            return
        return response.json()
