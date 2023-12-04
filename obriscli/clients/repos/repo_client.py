from ..base_client import BaseRESTClient
from .repo_response_mapper import RepoResponseMapper

from .routes import RepoPath


class RepoClient(BaseRESTClient):

    def list(self):
        response_json = self.get(RepoPath.REPOS.value)
        repos = response_json["repos"]
        formatted_response = RepoResponseMapper.repos(repos)
        return formatted_response

    def create(self):
        pass
