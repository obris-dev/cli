from enum import Enum


class WebserverPath(Enum):
    WEBSERVERS = "/compute/webservers"
    COMPUTE_TMPL = "/compute/{}"
