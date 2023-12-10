import attrs


@attrs.define
class Application:
    id: str
    account_id: str
    name: str
    provider: str
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
    updated_at: str
    created_at: str


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
    updated_at: str
    created_at: str


@attrs.define
class RuntimeType:
    type: str
    name: str


@attrs.define
class RuntimeVersion:
    id: str
    type: str
    name: str


@attrs.define
class Compute:
    id: str
    name: str
    human_status: str
    status: str
    domain: str
    has_tls: str
    process_ids: str
    instance_type: str
    keypair: str
    runtime: str
    availability_zones: str
    pre_cloud_init_script: str
    build_script: str
    post_build_script: str
    account_id: str
    application_id: str
    updated_at: str
    created_at: str


@attrs.define
class Runtime:
    id: str
    name: str


@attrs.define
class AvailabilityZone:
    id: str
    name: str


@attrs.define
class KeyPair:
    id: str
    name: str


@attrs.define
class InstanceType:
    id: str
    name: str


@attrs.define
class EnvironmentVariable:
    id: str
    application_id: str
    key: str
    value: str
    updated_at: str
    created_at: str


@attrs.define
class SSLTLSCertficate:
    id: str
    common_name: str
    domains: list[str]
    signature_algorithm: str
    serial_number: str
    not_before: str
    not_after: str
    updated_at: str
    created_at: str
