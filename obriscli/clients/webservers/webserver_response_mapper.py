from obriscli.clients.response_mappers import (
    Compute,
    Runtime,
    AvailabilityZone,
    KeyPair,
    InstanceType
)


class WebserverResponseMapper:

    @classmethod
    def webservers(cls, response_json):
        formatted_webservers = []
        for unformatted_webserver in response_json:
            formatted_webserver = cls.webserver(unformatted_webserver)
            formatted_webservers.append(formatted_webserver)
        return formatted_webservers

    @staticmethod
    def webserver(response_json):
        unformatted_webserver = response_json
        return Compute(
            unformatted_webserver["id"],
            unformatted_webserver["name"],
            unformatted_webserver["humanStatus"],
            unformatted_webserver["status"],
            unformatted_webserver["domain"],
            unformatted_webserver["hasTls"],
            unformatted_webserver["selectedProcessIds"],
            unformatted_webserver["instanceType"],
            unformatted_webserver["keypair"],
            unformatted_webserver["runtime"],
            unformatted_webserver["availabilityZones"],
            unformatted_webserver["preCloudInit"],
            unformatted_webserver["preProcessInit"],
            unformatted_webserver["postCloudInit"],
            unformatted_webserver["accountId"],
            unformatted_webserver["applicationId"],
            unformatted_webserver["updated"],
            unformatted_webserver["created"]
        )

    @classmethod
    def runtimes(cls, response_json):
        formatted_runtimes = []
        for unformatted_runtime in response_json:
            formatted_runtime = cls.runtime(unformatted_runtime)
            formatted_runtimes.append(formatted_runtime)
        return formatted_runtimes

    @staticmethod
    def runtime(response_json):
        unformatted_runtime = response_json
        return Runtime(
            unformatted_runtime["id"],
            unformatted_runtime["name"]
        )

    @classmethod
    def availability_zones(cls, response_json):
        formatted_availability_zones = []
        for unformatted_availability_zone in response_json:
            formatted_availability_zone = cls.availability_zone(unformatted_availability_zone)
            formatted_availability_zones.append(formatted_availability_zone)
        return formatted_availability_zones

    @staticmethod
    def availability_zone(response_json):
        unformatted_availability_zone = response_json
        return AvailabilityZone(
            unformatted_availability_zone,
            unformatted_availability_zone
        )

    @classmethod
    def key_pairs(cls, response_json):
        formatted_key_pairs = []
        for unformatted_key_pair in response_json:
            formatted_key_pair = cls.key_pair(unformatted_key_pair)
            formatted_key_pairs.append(formatted_key_pair)
        return formatted_key_pairs

    @staticmethod
    def key_pair(response_json):
        unformatted_key_pair = response_json
        return KeyPair(
            unformatted_key_pair["id"],
            unformatted_key_pair["keyPair"]
        )

    @classmethod
    def instance_types(cls, response_json):
        formatted_instance_types = []
        for unformatted_instance_type in response_json:
            formatted_instance_type = cls.instance_type(unformatted_instance_type)
            formatted_instance_types.append(formatted_instance_type)
        return formatted_instance_types

    @staticmethod
    def instance_type(response_json):
        unformatted_instance_type = response_json
        return InstanceType(
            unformatted_instance_type,
            unformatted_instance_type
        )
