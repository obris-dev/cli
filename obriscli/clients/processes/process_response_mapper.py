from obriscli.clients.response_mappers import (
    Process,
    RuntimeType,
    RuntimeVersion,
)


class ProcessResponseMapper:

    @classmethod
    def processes(cls, response_json):
        formatted_processes = []
        for unformatted_process in response_json:
            formatted_process = cls.process(unformatted_process)
            formatted_processes.append(formatted_process)
        return formatted_processes

    @staticmethod
    def process(response_json):
        unformatted_process = response_json
        return Process(
            unformatted_process["id"],
            unformatted_process["runtimeType"],
            unformatted_process["runtime"],
            unformatted_process["requirementsPath"],
            unformatted_process["procfilePath"],
            unformatted_process["localPort"],
            unformatted_process["routeMatch"],
            unformatted_process["accountId"],
            unformatted_process["applicationId"],
            unformatted_process["repositoryId"],
            unformatted_process["updated"],
            unformatted_process["created"]
        )

    @classmethod
    def runtime_types(cls, response_json):
        formatted_runtime_types = []
        for unformatted_runtime_type in response_json:
            formatted_runtime_type = cls.runtime_type(unformatted_runtime_type)
            formatted_runtime_types.append(formatted_runtime_type)
        return formatted_runtime_types

    @staticmethod
    def runtime_type(response_json):
        unformatted_runtime_type = response_json
        return RuntimeType(
            unformatted_runtime_type["id"],
            unformatted_runtime_type["name"]
        )

    @classmethod
    def runtimes(cls, response_json):
        formatted_runtimes = []
        for unformatted_runtime in response_json:
            formatted_runtime = cls.runtime(unformatted_runtime)
            formatted_runtimes.append(formatted_runtime)
        return formatted_runtimes

    @staticmethod
    def runtime(response_json):
        unformatted_runtime = response_json
        return RuntimeVersion(
            unformatted_runtime["id"],
            unformatted_runtime["type"],
            unformatted_runtime["name"]
        )
