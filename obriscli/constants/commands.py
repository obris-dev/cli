from enum import Enum


class CommandOption(Enum):
    APPLICATION = "application"
    CERTIFICATE = "certificate"
    CLOUD_APPLICATION = "cloud_application"
    CREDENTIAL = "credential"
    CREDENTIAL_GITHUB = "credential_github"
    ENV_VAR = "env_var"
    PROCESS = "process"
    REPO = "repo"
    WEBSERVER = "webserver"
