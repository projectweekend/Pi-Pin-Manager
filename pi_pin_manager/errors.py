class PinNotDefinedError(Exception):
    pass


class PinConfigurationError(Exception):
    pass


class InvalidConfigurationError(Exception):

    def __init__(self, message, errors):
        super(InvalidConfigurationError, self).__init__(message)
        self.errors = errors
