from ..response_mappers import Application


class ApplicationResponseMapper:

    @classmethod
    def applications(cls, response_json):
        formatted_resp = []
        for unformatted_resp in response_json:
            unformatted_resp = cls.application(unformatted_resp)
            formatted_resp.append(unformatted_resp)
        return formatted_resp

    @staticmethod
    def application(response_json):
        unformatted_resp = response_json
        return Application(
            unformatted_resp["id"],
            unformatted_resp["accountId"],
            unformatted_resp["name"],
            unformatted_resp["region"],
            unformatted_resp["description"],
            unformatted_resp["hasCredentials"],
            unformatted_resp["created"]
        )
