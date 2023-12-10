from .clients import (
    ApplicationClient,
    CloudApplicationClient,
    EnvVarCredentialClient,
    GithubCredentialClient,
    NotifyClient,
    ProcessClient,
    RepoClient,
    SSLTLSCertificateClient,
    WebserverClient,
)
from .constants import CommandOption


COMMAND_TO_CLIENT = {
    CommandOption.APPLICATION: ApplicationClient,
    CommandOption.CERTIFICATE: SSLTLSCertificateClient,
    CommandOption.CLOUD_APPLICATION: CloudApplicationClient,
    CommandOption.CREDENTIAL_GITHUB: GithubCredentialClient,
    CommandOption.ENV_VAR: EnvVarCredentialClient,
    CommandOption.NOTIFY: NotifyClient,
    CommandOption.PROCESS: ProcessClient,
    CommandOption.REPO: RepoClient,
    CommandOption.WEBSERVER: WebserverClient
}


class ClientFactory:
    def __init__(self, access_token, base_url):
        self.access_token = access_token
        self.base_url = base_url
        self.base_v1_api_url = f"{self.base_url}/v1"

    def create_client(self, command):
        command_client = COMMAND_TO_CLIENT[command]
        return command_client(
            access_token=self.access_token,
            base_api_url=self.base_v1_api_url
        )
