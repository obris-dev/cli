import webbrowser

from enum import Enum
from urllib.parse import urlencode
from time import sleep

from obriscli.logger import Logger
from obriscli.utilities import make_id

from ..notify import NotifyClient
from .application_client import ApplicationClient
from .exceptions import (
    ApplicationAlreadyLinkedError,
    ProviderNotReleasedError
)

from ..users import UserClient

logger = Logger()


class IntegrationDestinationURL(Enum):
    CLOUD_FORMATION = "https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate"


class TemplateURL(Enum):
    CLOUD_FORMATION = "https://obris-public-v1.s3.amazonaws.com/functions/obris.template.yaml"


class CloudApplicationClient(ApplicationClient):

    def __init__(self, access_token, base_api_url):
        super().__init__(access_token, base_api_url)
        self.__user_client = None
        self.__notify_client = None

    @property
    def user_client(self):
        if self.__user_client is None:
            self.__user_client = UserClient(self.access_token, self.base_api_url)
        return self.__user_client

    @property
    def notify_client(self):
        if self.__notify_client is None:
            self.__notify_client = NotifyClient(self.access_token, self.base_api_url)
        return self.__notify_client

    @staticmethod
    def __generate_cloud_name():
        placeholder_cloud_name_template = "obris-stack-{}"
        uniq_id = make_id(6, case_sensitive=False)
        return placeholder_cloud_name_template.format(uniq_id)

    def __generate_link_params(self, user, application):
        placeholder_name = self.__generate_cloud_name()
        return {
            "templateURL": TemplateURL.CLOUD_FORMATION.value,
            "stackName": placeholder_name,
            "param_AccountId": application.account_id,
            "param_ApplicationName": application.name,
            "param_ApplicationId": application.id,
            "param_Username": user.email
        }

    def are_unlinked(self):
        return self.list(has_credentials=False)

    def link(self, pk=None):
        self.start_link(pk=pk)

    def start_link(self, pk=None):
        if pk is None:
            raise ValueError("id is required.")

        application = self.get_one(pk=pk)
        if application.has_credentials:
            raise ApplicationAlreadyLinkedError(f"Application already linked: id={pk}")

        if application.provider in (1, 2,):
            raise ProviderNotReleasedError(
                f"{application.human_provider} is still being implemented!",
                application.provider,
                application.human_provider
            )

        logger.log(f"Linking application id={application.id} name={application.name}...  "
                   f"Redirecting to {application.human_provider} to complete the process.\n")
        sleep(1)

        user = self.user_client.self()

        query_params = self.__generate_link_params(user, application)

        destination_url = IntegrationDestinationURL.CLOUD_FORMATION.value
        encoded_params = urlencode(query_params)
        integration_destination = f"{destination_url}?{encoded_params}"
        webbrowser.open(integration_destination)

    def poll_link(self, pk=None):
        if pk is None:
            raise ValueError("id is required.")

        sleep_secs = 15
        timeout = 60 * 15  # 15 minutes
        while True:
            application = self.get_one(pk=pk)
            if application.has_credentials:
                logger.log(f"Application linked!\n")
                return True
            elif timeout <= 0:
                logger.log(f"Timeout waiting for application link.\n", error=True)
                return False
            logger.log(f"Application not yet linked. Checking again in {sleep_secs}s...\n")
            sleep(sleep_secs)
            timeout -= sleep_secs

    def notify_on_link_release(self, provider=None):
        if provider is None:
            raise ValueError("missing provider")

        self.notify_client.create(kind="new_link", provider=provider)
