from enum import Enum


class ProcessPath(Enum):
    PROCESSES = "/compute/processes"
    PROCESS_TMPL = "/compute/process/{}"
    RUNTIME_TYPES_TMPL = "/applications/{}/runtime-types"
    RUNTIMES_TMPL = "/applications/{}/runtime/{}/versions"
