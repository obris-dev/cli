from ..base_client import BaseRESTClient
from .repo_response_mapper import RepoResponseMapper


class RepoClient(BaseRESTClient):

    def list(self):
        response_json = self.get("/credentials/repos")
        repos = response_json["repos"]
        formatted_response = RepoResponseMapper.list_of_repos(repos)
        return formatted_response
