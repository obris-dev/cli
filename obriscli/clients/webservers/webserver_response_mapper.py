from obriscli.clients.response_mappers import Compute


class WebserverResponseMapper:

    @classmethod
    def webservers(cls, response_json):
        formatted_webservers = []
        for unformatted_webserver in response_json:
            formatted_webserver = cls.webserver(unformatted_webserver)
            formatted_webservers.append(formatted_webserver)
        return formatted_webservers

    @staticmethod
    def webserver(response_json):
        unformatted_webserver = response_json
        return Compute(
            unformatted_webserver["id"],
            unformatted_webserver["name"],
            unformatted_webserver["humanStatus"],
            unformatted_webserver["status"],
            unformatted_webserver["domain"],
            unformatted_webserver["hasTls"],
            unformatted_webserver["selectedProcessIds"],
            unformatted_webserver["instanceType"],
            unformatted_webserver["keypair"],
            unformatted_webserver["runtime"],
            unformatted_webserver["availabilityZones"],
            unformatted_webserver["preCloudInit"],
            unformatted_webserver["preProcessInit"],
            unformatted_webserver["postCloudInit"],
            unformatted_webserver["accountId"],
            unformatted_webserver["applicationId"],
            unformatted_webserver["updated"],
            unformatted_webserver["created"]
        )
