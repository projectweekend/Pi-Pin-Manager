import yaml
from validation import ConfigValidator, CONFIG_SCHEMA
from errors import PinNotDefinedError, InvalidConfigurationError


class GPIOConfig(object):

    def __init__(self, config, event_handler=None):
        self._config = config
        self._event_handler = event_handler
        self._load_pin_config()

    def _load_pin_config(self):
        if isinstance(self._config, list):
            self._pin_config = self._config
        else:
            with open(self._config) as file:
                self._pin_config = yaml.safe_load(file)
        v = ConfigValidator(CONFIG_SCHEMA)
        for item in self._pin_config:
            if not v.validate(item):
                message = "Invalid configuration file/dictionary. Check 'errors' for detail."
                raise InvalidConfigurationError(message, v.errors)

    def get_config(self, pin_number=None):

        def has_pin(item):
            return item['pin'] == pin_number

        if pin_number:
            matched = filter(has_pin, self._pin_config)
            if not matched:
                message = "Pin {0} is not defined".format(pin_number)
                raise PinNotDefinedError(message)
            return [i.copy() for i in matched]
        return [i.copy() for i in self._pin_config]
