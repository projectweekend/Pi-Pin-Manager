import yaml
import RPi.GPIO as GPIO

from exceptions import PinConfigurationError, PinNotDefinedError


class Configurable(object):

    def __init__(self, config_file=None, config_dict=None, event_handlers=None):
        self.config_file = config_file
        self.config_dict = config_dict
        self.event_handlers = event_handlers
        self._load_pin_config()

    def _load_pin_config(self):
        if not self.config_file and not self.config_dict:
            message = "PinManager requires either a 'config_file' or 'config_dict' parameter"
            raise PinConfigurationError(message)
        if self.config_file:
            self._configure_from_file()
        else:
            self._configure_from_dict()

    def _configure_from_file(self):
        with open(self.config_file) as file_data:
            self.pin_config = yaml.safe_load(file_data)

    def _configure_from_dict(self):
        if type(self.config_dict) != 'dict':
            message = "'config_dict' parameter must be a dictionary"
            raise PinConfigurationError(message)
        self.pin_config = self.config_dict

    def get_config(self, pin_number=None):
        if pin_number:
            try:
                return self.pin_config[pin_number].copy()
            except KeyError:
                message = "Pin {0} not defined in configuration".format(pin_number)
                raise PinNotDefinedError(message)
        return self.pin_config.copy()


class GPIOSetup(object):

    def _initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._gpio = GPIO
        if self.event_handlers:
            self.event_handlers = self.event_handlers(self._gpio)

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
            handler = self.event_handlers.__getattribute__(handler)
            self._gpio.add_event_detect(number, event, callback=handler, bouncetime=bounce)

    def cleanup(self, pin_number=None):
        if pin_number:
            return self._gpio.cleanup(pin_number)
        return self._gpio.cleanup()
