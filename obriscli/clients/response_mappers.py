import attrs


@attrs.define
class Application:
    id: str
    account_id: str
    name: str
    region: str
    description: str
    has_credentials: bool
    created_at: str


@attrs.define
class Repo:
    id: str
    name: str
    url: str
    user_id: str
    account_id: str
    application_id: str
    credential_id: str
    created_at: str
    updated_at: str


@attrs.define
class User:
    id: str
    email: str


@attrs.define
class Account:
    id: str
    name: str
    url: str
    user_id: str
    account_id: str
    application_id: str
    credential_id: str
    created_at: str
    updated_at: str


@attrs.define
class CredentialGithub:
    id: str
    username: str
    mask_token: str
    user_id: str
    account_id: str
    application_id: str
    updated_at: str
    created_at: str


@attrs.define
class Process:
    id: str
    runtime_type: str
    runtime: str
    requirements_path: str
    procfile_path: str
    local_port: str
    route_match: str
    account_id: str
    application_id: str
    repository_id: str
    updated: str
    created: str


@attrs.define
class RuntimeType:
    type: str
    name: str


@attrs.define
class RuntimeVersion:
    id: str
    type: str
    name: str
