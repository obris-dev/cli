class ApplicationAlreadyLinkedError(ValueError):
    pass


class ProviderNotReleasedError(NotImplementedError):
    def __init__(self, msg, unimplemented_provider, unimplemented_human_provider):
        self.msg = msg
        self.unimplemented_provider = unimplemented_provider
        self.unimplemented_human_provider = unimplemented_human_provider
