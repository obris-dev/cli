from obriscli.clients.response_mappers import Repo


class RepoResponseMapper:

    @classmethod
    def repos(cls, response_json):
        formatted_repos = []
        for unformatted_repo in response_json:
            formatted_repo = cls.repo(unformatted_repo)
            formatted_repos.append(formatted_repo)
        return formatted_repos

    @staticmethod
    def repo(response_json):
        unformatted_repo = response_json
        return Repo(
            unformatted_repo["id"],
            unformatted_repo["name"],
            unformatted_repo["url"],
            unformatted_repo["userId"],
            unformatted_repo["accountId"],
            unformatted_repo["applicationId"],
            unformatted_repo["credentialId"],
            unformatted_repo["updated"],
            unformatted_repo["created"]
        )
