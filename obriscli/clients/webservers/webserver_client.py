import json

from ..base_client import BaseRESTClient

from .routes import WebserverPath
from .webserver_response_mapper import WebserverResponseMapper


MAX_SERVER_NAME = 245


class WebserverClient(BaseRESTClient):

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
            post_process_init_script=None
    ):
        if application_id is None:
            raise ValueError("missing application_id")

        if name is None:
            raise ValueError("missing name")
        elif len(name) > MAX_SERVER_NAME:
            raise ValueError("Provided name is too long")

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
        if post_process_init_script is not None:
            data["post_cloud_init_script"] = post_process_init_script

        response_json = self.post(WebserverPath.WEBSERVERS.value, data=data)
        webserver = response_json["webserver"]
        formatted_response = WebserverResponseMapper.webserver(webserver)
        return formatted_response
