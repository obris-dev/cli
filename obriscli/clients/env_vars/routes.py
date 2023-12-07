from enum import Enum


class EnvVarPath(Enum):
    ENV_VARS_TMPL = "/config/{}/vars"
    ENV_VAR_TMPL = "/config/{}/var/{}"
