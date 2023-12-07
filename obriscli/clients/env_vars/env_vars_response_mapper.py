from obriscli.clients.response_mappers import (
    EnvironmentVariable
)


class EnvVarResponseMapper:

    @classmethod
    def variables(cls, response_json):
        formatted_variables = []
        for unformatted_variable in response_json:
            formatted_variable = cls.variable(unformatted_variable)
            formatted_variables.append(formatted_variable)
        return formatted_variables

    @staticmethod
    def variable(response_json):
        return EnvironmentVariable(
            response_json["id"],
            response_json["applicationId"],
            response_json["key"],
            response_json["value"],
            response_json["updated"],
            response_json["created"],
        )
