import attrs


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
