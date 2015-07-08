import yaml
from cerberus import Validator
import RPi.GPIO as GPIO
from exceptions import PinNotDefinedError, InvalidConfigurationError


CONFIG_SCHEMA = {
    'mode': {
        'type': 'string',
        'is_pin_mode': True
    },
    'initial': {
        'type': 'string',
        'required': False,
        'is_initial': True
    },
    'resistor': {
        'type': 'string',
        'required': False,
        'is_resistor': True
    },
    'event': {
        'type': 'string',
        'required': False,
        'is_event': True
    },
    'handler': {
        'type': 'string',
        'required': False
    },
    'bounce': {
        'type': 'integer',
        'required': False,
    }
}


class ConfigValidator(Validator):

    def _validate_is_pin_mode(self, is_pin_mode, field, value):
        modes = ('IN', 'OUT', )
        if is_pin_mode and not value in modes:
            message = "Must be one of: {0}".format(', '.join(modes))
            self._error(field, message)

    def _validate_is_initial(self, is_initial, field, value):
        initial_values = ('LOW', 'HIGH', )
        if is_initial and not value in initial_values:
            message = "Must be one of: {0}".format(', '.join(initial_values))
            self._error(field, message)

    def _validate_is_resistor(self, is_resistor, field, value):
        resistor_values = ('PUD_UP', 'PUD_DOWN', )
        if is_resistor and not value in resistor_values:
            message = "Must be one of: {0}".format(', '.join(resistor_values))
            self._error(field, message)


class GPIOConfig(object):

    def __init__(self, config, event_handler=None):
        self._config = config
        self._event_handler = event_handler
        self._load_pin_config()

    def _load_pin_config(self):
        if isinstance(self._config, dict):
            self._pin_config = self._config
        else:
            with open(self._config) as file:
                self._pin_config = yaml.safe_load(file)
        v = ConfigValidator(CONFIG_SCHEMA)
        if not v.validate(self._pin_config):
            message = "Invalid configuration file/dictionary. Check 'errors' for detail."
            raise InvalidConfigurationError(message, v.errors)

    def get_config(self, pin_number=None):
        if pin_number:
            try:
                return self._pin_config[pin_number].copy()
            except KeyError:
                message = "Pin {0} not defined in configuration".format(pin_number)
                raise PinNotDefinedError(message)
        return self._pin_config.copy()


class GPIOActions(object):

    def _initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._gpio = GPIO
        if self._event_handler:
            self._event_handler = self._event_handler(self._gpio)

    def _setup_pin(self, number, options):
        mode = self._gpio.__getattribute__(options['mode'])
        initial = self._gpio.__getattribute__(options.get('initial', 'LOW'))
        resistor = options.get('resistor', None)
        if resistor:
            resistor = self._gpio.__getattribute__(resistor)
            self._gpio.setup(number, mode, initial=initial, pull_up_down=resistor)
        else:
            self._gpio.setup(number, mode, initial=initial)

        event = options.get('event', None)
        handler = options.get('handler', None)
        bounce = options.get('bounce', 0)
        if event and handler:
            event = self._gpio.__getattribute__(event)
            handler = self._event_handler.__getattribute__(handler)
            self._gpio.add_event_detect(number, event, callback=handler, bouncetime=bounce)

    def cleanup(self, pin_number=None):
        if pin_number:
            return self._gpio.cleanup(pin_number)
        return self._gpio.cleanup()
