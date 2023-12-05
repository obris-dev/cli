from ...base_client import BaseRESTClient
from .routes import CredentialGithubPath
from .github_credential_response_mapper import CredentialGithubResponseMapper


class GithubCredentialClient(BaseRESTClient):

    def list(self, application_id=None):
        query_params = {}
        if application_id is not None:
            query_params["application_id"] = application_id

        response_json = self.get(CredentialGithubPath.GITHUBS.value, params=query_params)
        credential = response_json["credential"]
        if credential is None:
            return None
        formatted_response = CredentialGithubResponseMapper.credential(credential)
        return formatted_response

    def create(self, application_id=None, username=None, token=None):
        if application_id is None:
            raise ValueError("missing application_id")
        if username is None:
            raise ValueError("missing username")
        if token is None:
            raise ValueError("missing token")

        data_params = {
            "application_id": application_id,
            "username": username,
            "token": token,
        }
        response_json = self.post(CredentialGithubPath.GITHUBS.value, data=data_params)
        credential = response_json["credential"]
        formatted_response = CredentialGithubResponseMapper.credential(credential)
        return formatted_response

    def delete(self, pk=None):
        if pk is None:
            raise ValueError("missing id")
        command_path = CredentialGithubPath.GITHUB.value.format(pk)
        super().delete(command_path)
