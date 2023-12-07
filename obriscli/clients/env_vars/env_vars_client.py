from ..base_client import BaseRESTClient
from .routes import EnvVarPath
from .env_vars_response_mapper import EnvVarResponseMapper


class EnvVarCredentialClient(BaseRESTClient):

    def list(self, application_id=None):
        if application_id is None:
            raise ValueError("missing application_id")

        command_path = EnvVarPath.ENV_VARS_TMPL.value.format(application_id)
        response_json = self.get(command_path)
        variables = response_json["variables"]
        formatted_response = EnvVarResponseMapper.variables(variables)
        return formatted_response

    def create(self, application_id=None, key=None, value=None):
        if application_id is None:
            raise ValueError("missing application_id")
        if key is None:
            raise ValueError("missing key")
        if value is None:
            raise ValueError("missing value")

        data = {
            "key": key,
            "value": value
        }
        command_path = EnvVarPath.ENV_VARS_TMPL.value.format(application_id)
        response_json = self.post(command_path, data)
        variable = response_json["variable"]
        formatted_response = EnvVarResponseMapper.variable(variable)
        return formatted_response

    def update(self, pk=None, application_id=None, key=None, value=None):
        if pk is None:
            raise ValueError("missing id")
        if application_id is None:
            raise ValueError("missing application_id")

        data = {}
        if key is not None:
            data["key"] = key
        if value is not None:
            data["value"] = value

        command_path = EnvVarPath.ENV_VAR_TMPL.value.format(application_id, pk)
        response_json = self.put(command_path, data)
        variable = response_json["variable"]
        formatted_response = EnvVarResponseMapper.variable(variable)
        return formatted_response

    def delete(self, pk=None, application_id=None):
        if pk is None:
            raise ValueError("missing id")

        if application_id is None:
            raise ValueError("missing application_id")

        command_path = EnvVarPath.ENV_VAR_TMPL.value.format(application_id, pk)
        return super().delete(command_path)
