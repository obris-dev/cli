from enum import Enum


class WebserverPath(Enum):
    WEBSERVERS = "/compute/webservers"
    COMPUTE_TMPL = "/compute/{}"

    RUNTIMES_TMPL = "/applications/{}/runtimes"
    AVAILABILITY_ZONES_TMPL = "/applications/{}/availability-zones"
    INSTANCE_TYPES_TMPL = "/applications/{}/instance-types"
    KEY_PAIRS_TMPL = "/applications/{}/key-pairs"
