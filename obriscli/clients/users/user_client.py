from ..base_client import BaseRESTClient
from .user_response_mapper import UserResponseMapper

from .routes import UserPath


class UserClient(BaseRESTClient):

    def self(self):
        response_json = self.get(UserPath.USER.value)
        user = response_json["user"]
        formatted_response = UserResponseMapper.user(user)
        return formatted_response
