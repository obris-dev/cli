from ..base_client import BaseRESTClient
from .process_response_mapper import ProcessResponseMapper

from .routes import ProcessPath


class ProcessClient(BaseRESTClient):

    def list(self, application_id=None):
        query_params = {}
        if application_id is not None:
            query_params["application_id"] = application_id

        response_json = self.get(ProcessPath.PROCESSES.value, params=query_params)
        processes = response_json["processes"]
        formatted_response = ProcessResponseMapper.processes(processes)
        return formatted_response

    def create(
            self,
            application_id=None,
            repository_id=None,
            runtime=None,
            requirements_path=None,
            procfile_path=None,
            local_port=None,
            route_match=None
    ):
        if application_id is None:
            raise ValueError("missing application_id")
        if repository_id is None:
            raise ValueError("missing repository_id")
        if runtime is None:
            raise ValueError("missing runtime")
        if requirements_path is None:
            raise ValueError("missing requirements_path")
        if procfile_path is None:
            raise ValueError("missing procfile_path")

        data = {
            "application_id": application_id,
            "repository_id": repository_id,
            "runtime": runtime,
            "requirements_path": requirements_path,
            "procfile_path": procfile_path,
        }

        if local_port is not None:
            data["local_port"] = local_port
        if route_match is not None:
            data["route_match"] = route_match

        response_json = self.post(ProcessPath.PROCESSES.value, data=data)
        process = response_json["process"]
        formatted_response = ProcessResponseMapper.process(process)
        return formatted_response

    def update(
            self,
            pk=None,
            repository_id=None,
            runtime=None,
            requirements_path=None,
            procfile_path=None,
            local_port=None,
            route_match=None
    ):
        if pk is None:
            raise ValueError("missing id")

        data = {}
        if repository_id is not None:
            data["repository_id"] = repository_id
        if runtime is not None:
            data["runtime"] = runtime
        if requirements_path is not None:
            data["requirements_path"] = requirements_path
        if procfile_path is not None:
            data["procfile_path"] = procfile_path
        if local_port is not None:
            data["local_port"] = local_port
        if route_match is not None:
            data["route_match"] = route_match

        command_path = ProcessPath.PROCESS_TMPL.value.format(pk)
        response_json = self.put(command_path, data=data)
        process = response_json["process"]
        formatted_response = ProcessResponseMapper.process(process)
        return formatted_response

    def delete(self, pk=None):
        if pk is None:
            raise ValueError("missing id")

        command_path = ProcessPath.PROCESS_TMPL.value.format(pk)
        super().delete(command_path)

    def clear_route_config(self, pk=None):
        if pk is None:
            raise ValueError("missing id")

        data = {
            "local_port": 0,
            "route_match": 0
        }
        command_path = ProcessPath.PROCESS_TMPL.value.format(pk)
        response_json = self.put(command_path, data=data)
        process = response_json["process"]
        formatted_response = ProcessResponseMapper.process(process)
        return formatted_response

    def runtime_types(self, application_id=None):
        if application_id is None:
            raise ValueError("missing application_id")
        command_path = ProcessPath.RUNTIME_TYPES_TMPL.value.format(application_id)
        response_json = self.get(command_path)
        runtime_types = response_json["runtimeTypes"]
        formatted_response = ProcessResponseMapper.runtime_types(runtime_types)
        return formatted_response

    def runtimes(self, application_id=None, runtime_type=None):
        if application_id is None:
            raise ValueError("missing application_id")
        if runtime_type is None:
            raise ValueError("missing runtime_type")

        command_path = ProcessPath.RUNTIMES_TMPL.value.format(application_id, runtime_type)
        response_json = self.get(command_path)
        runtime_types = response_json["runtimeVersions"]
        formatted_response = ProcessResponseMapper.runtimes(runtime_types)
        return formatted_response
