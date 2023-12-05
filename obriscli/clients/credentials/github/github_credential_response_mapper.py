from obriscli.clients.response_mappers import CredentialGithub


class CredentialGithubResponseMapper:

    @classmethod
    def credentials(cls, response_json):
        formatted_credentials = []
        for formatted_credential in response_json:
            formatted_credential = cls.credential(formatted_credential)
            formatted_credentials.append(formatted_credential)
        return formatted_credentials

    @staticmethod
    def credential(response_json):
        unformatted_credential = response_json
        print(unformatted_credential)
        return CredentialGithub(
            unformatted_credential["id"],
            unformatted_credential["username"],
            unformatted_credential["maskToken"],
            unformatted_credential["userId"],
            unformatted_credential["accountId"],
            unformatted_credential["applicationId"],
            unformatted_credential["updated"],
            unformatted_credential["created"]
        )
