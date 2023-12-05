from ..base_client import BaseRESTClient
from .repo_response_mapper import RepoResponseMapper

from .routes import RepoPath


class RepoClient(BaseRESTClient):

    def list(self, application_id=None):
        query_params = {}
        if application_id is not None:
            query_params["application_id"] = application_id

        response_json = self.get(RepoPath.REPOS.value, params=query_params)
        repos = response_json["repos"]
        formatted_response = RepoResponseMapper.repos(repos)
        return formatted_response

    def create(self, application_id=None, url=None, name=None, credential_id=None):
        if application_id is None:
            raise ValueError("missing application_id")
        if url is None:
            raise ValueError("missing url")
        if name is None:
            raise ValueError("missing name")

        data_params = {
            "application_id": application_id,
            "url": url,
            "name": name,
        }
        if credential_id is not None:
            data_params["credential_id"] = credential_id

        response_json = self.post(RepoPath.REPOS.value, data=data_params)
        repo = response_json["repo"]
        formatted_response = RepoResponseMapper.repo(repo)

        return formatted_response

    def update(self, pk=None, url=None, name=None, credential_id=None):
        if pk is None:
            raise ValueError("missing id")

        data_params = {}
        if url is not None:
            data_params["url"] = url
        if name is not None:
            data_params["name"] = name
        if credential_id is not None:
            data_params["credential_id"] = credential_id

        formatted_path = RepoPath.REPO.value.format(pk)
        response_json = self.put(formatted_path, data=data_params)
        repo = response_json["repo"]
        formatted_response = RepoResponseMapper.repo(repo)
        return formatted_response

    def delete(self, pk=None):
        if pk is None:
            raise ValueError("missing id")

        formatted_path = RepoPath.REPO.value.format(pk)
        super().delete(formatted_path)

    def clear_credential(self, pk=None):
        if pk is None:
            raise ValueError("missing id")

        data_params = {
            "credential_id": 0
        }
        formatted_path = RepoPath.REPO.value.format(pk)
        response_json = self.put(formatted_path, data=data_params)
        repo = response_json["repo"]
        formatted_response = RepoResponseMapper.repo(repo)
        return formatted_response
