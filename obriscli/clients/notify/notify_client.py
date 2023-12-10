from ..base_client import BaseRESTClient

from .routes import NotifyPath


class NotifyClient(BaseRESTClient):

    def create(self, kind=None, provider=None):
        if kind is None:
            raise ValueError("missing kind string")
        if provider is None:
            raise ValueError("missing provider")

        data = {
            "kind": kind,
            "source": "cli",
            "link_type": provider
        }
        command_path = NotifyPath.NOTIFY.value
        self.post(command_path, data)
