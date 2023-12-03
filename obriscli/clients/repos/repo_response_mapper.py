from .response_mappers import Repo


class RepoResponseMapper:

    @staticmethod
    def list_of_repos(response):
        formatted_repos = []
        for unformatted_repo in response:
            formatted_repo = Repo(
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
            formatted_repos.append(formatted_repo)
        return formatted_repos
