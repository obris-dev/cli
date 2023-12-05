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

    def create(self):
        pass
