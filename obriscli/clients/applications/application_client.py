from enum import Enum

from ..base_client import BaseRESTClient

from .application_response_mapper import ApplicationResponseMapper
from .routes import ApplicationPath


class ApplicationType(Enum):
    AWS = 0
    AZURE = 1
    GCP = 2


class ApplicationClient(BaseRESTClient):

    @staticmethod
    def __map_provider_type(provider_slug):
        return ApplicationType[provider_slug.upper()].value

    def list(self, has_credentials=None):
        query_params = {}
        if has_credentials is not None:
            query_params["has_credentials"] = has_credentials

        response_json = self.get(ApplicationPath.APPLICATIONS.value, params=query_params)
        applications = response_json["applications"]
        formatted_response = ApplicationResponseMapper.applications(applications)
        return formatted_response

    def get_one(self, pk=None):
        if pk is None:
            raise ValueError("id is missing.")

        application_path_format_str = ApplicationPath.APPLICATION.value
        application_path = application_path_format_str.format(pk)

        response_json = self.get(application_path)

        application = response_json["application"]
        formatted_response = ApplicationResponseMapper.application(application)
        return formatted_response

    def create(self, name=None, provider=None, region=None, description=None):
        if name is None:
            raise ValueError("missing name.")
        if provider is None:
            raise ValueError("missing provider.")
        if region is None:
            raise ValueError("missing region.")

        provider_type = self.__map_provider_type(provider)
        data = {
            "type": provider_type,
            "name": name,
            "region": region,
            "description": description,
        }
        response_json = self.post(ApplicationPath.APPLICATIONS.value, data)
        application = response_json["application"]
        formatted_response = ApplicationResponseMapper.application(application)
        return formatted_response

    def update(self, pk=None, name=None, description=None):
        if pk is None:
            raise ValueError("Missing id field.")

        if name is None and description is None:
            raise ValueError("Missing arguments 'name', or 'description'.")

        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description

        application_path_format_str = ApplicationPath.APPLICATION.value
        application_path = application_path_format_str.format(pk)
        response_json = self.put(application_path, data)
        application = response_json["application"]
        formatted_response = ApplicationResponseMapper.application(application)
        return formatted_response

    def delete(self, pk=None):
        if pk is None:
            raise ValueError("id is required.")

        application_path_format_str = ApplicationPath.APPLICATION.value
        application_path = application_path_format_str.format(pk)
        return super().delete(application_path)

    def regions(self, provider=None):
        if provider is None:
            raise ValueError("missing provider.")

        regions_path_format_str = ApplicationPath.REGIONS.value
        region_path = regions_path_format_str.format(provider)

        response_json = self.get(region_path)
        regions = response_json["regions"]
        return regions
