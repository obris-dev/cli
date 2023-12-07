import json

from ..base_client import BaseRESTClient

from .routes import WebserverPath
from .webserver_response_mapper import WebserverResponseMapper


MAX_SERVER_NAME = 245


class WebserverClient(BaseRESTClient):

    @staticmethod
    def __name_validator(name):
        if name is None:
            raise ValueError("missing name")
        elif len(name) > MAX_SERVER_NAME:
            raise ValueError("Provided name is too long")
        return name

    def list(self, application_id=None):
        if application_id is None:
            raise ValueError("missing application_id")

        query_params = {
            "application_id": application_id
        }
        response_json = self.get(WebserverPath.WEBSERVERS.value, params=query_params)
        webservers = response_json["webservers"]
        formatted_response = WebserverResponseMapper.webservers(webservers)
        return formatted_response

    def create(
            self,
            application_id=None,
            name=None,
            process_ids=None,
            instance_type=None,
            keypair=None,
            runtime=None,
            availability_zones=None,
            domain=None,
            pre_cloud_init_script=None,
            pre_process_init_script=None,
            post_cloud_init_script=None
    ):
        if application_id is None:
            raise ValueError("missing application_id")

        self.__name_validator(name)

        if process_ids is None:
            raise ValueError("missing process_ids")
        if instance_type is None:
            raise ValueError("missing instance_type")
        if keypair is None:
            raise ValueError("missing keypair")
        if runtime is None:
            raise ValueError("missing runtime")
        if availability_zones is None:
            raise ValueError("missing availability_zones")

        data = {
            "application_id": application_id,
            "name": name,
            "selected_process_ids": list(process_ids),
            "instance_type": instance_type,
            "keypair": keypair,
            "runtime": runtime,
            "availability_zones": list(availability_zones)
        }

        if domain is not None:
            data["domain"] = domain
        if pre_cloud_init_script is not None:
            data["pre_cloud_init_script"] = pre_cloud_init_script
        if pre_process_init_script is not None:
            data["pre_process_init_script"] = pre_process_init_script
        if post_cloud_init_script is not None:
            data["post_cloud_init_script"] = post_cloud_init_script

        response_json = self.post(WebserverPath.WEBSERVERS.value, data=data)
        webserver = response_json["webserver"]
        formatted_response = WebserverResponseMapper.webserver(webserver)
        return formatted_response

    def update(
            self,
            pk=None,
            name=None,
            process_ids=None,
            instance_type=None,
            keypair=None,
            runtime=None,
            availability_zones=None,
            domain=None,
            pre_cloud_init_script=None,
            pre_process_init_script=None,
            post_cloud_init_script=None
    ):
        data = {}
        if pk is None:
            raise ValueError("missing id")

        try:
            self.__name_validator(name)
            data["name"] = name
        except ValueError:
            raise

        if process_ids is not None:
            data["process_ids"] = process_ids
        if instance_type is not None:
            data["instance_type"] = instance_type
        if keypair is not None:
            data["keypair"] = keypair
        if runtime is not None:
            data["runtime"] = runtime
        if availability_zones is not None:
            data["availability_zones"] = availability_zones

        if domain is not None:
            data["domain"] = domain

        if pre_cloud_init_script is not None:
            data["pre_cloud_init_script"] = pre_cloud_init_script
        if pre_process_init_script is not None:
            data["pre_process_init_script"] = pre_process_init_script
        if post_cloud_init_script is not None:
            data["post_cloud_init_script"] = post_cloud_init_script

        command_path = WebserverPath.COMPUTE_TMPL.value.format(pk)
        response_json = self.put(command_path, data)
        webserver = response_json["compute"]
        formatted_response = WebserverResponseMapper.webserver(webserver)
        return formatted_response

    def delete(
            self,
            pk=None
    ):
        if pk is None:
            raise ValueError("missing id")

        command_path = WebserverPath.COMPUTE_TMPL.value.format(pk)
        super().delete(command_path)

    def runtimes(self, application_id=None):
        if application_id is None:
            raise ValueError("missing application_id")

        command_path = WebserverPath.RUNTIMES_TMPL.value.format(application_id)
        response_json = self.get(command_path)
        runtimes = response_json["runtimes"]
        formatted_response = WebserverResponseMapper.runtimes(runtimes)
        return formatted_response

    def availability_zones(self, application_id=None):
        if application_id is None:
            raise ValueError("missing application_id")

        command_path = WebserverPath.AVAILABILITY_ZONES_TMPL.value.format(application_id)
        response_json = self.get(command_path)
        availability_zones = response_json["availabilityZones"]
        formatted_response = WebserverResponseMapper.availability_zones(availability_zones)
        return formatted_response

    def key_pairs(self, application_id=None):
        if application_id is None:
            raise ValueError("missing application_id")

        command_path = WebserverPath.KEY_PAIRS_TMPL.value.format(application_id)
        response_json = self.get(command_path)
        key_pairs = response_json["keyPairs"]
        formatted_response = WebserverResponseMapper.key_pairs(key_pairs)
        return formatted_response

    def instance_types(self, application_id=None):
        if application_id is None:
            raise ValueError("missing application_id")

        command_path = WebserverPath.INSTANCE_TYPES_TMPL.value.format(application_id)
        response_json = self.get(command_path)
        instance_types = response_json["instanceTypes"]
        formatted_response = WebserverResponseMapper.instance_types(instance_types)
        return formatted_response
