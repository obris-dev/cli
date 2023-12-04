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
