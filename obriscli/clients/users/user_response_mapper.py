from ..response_mappers import User


class UserResponseMapper:
    @staticmethod
    def user(response_json):
        unformatted_user = response_json
        return User(
            unformatted_user["id"],
            unformatted_user["email"],
        )
