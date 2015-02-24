import yaml
import RPi.GPIO as GPIO

from exceptions import PinConfigurationError


class Configurable(object):

    def __init__(self, config_file=None, config_dict=None):
        self.config_file = config_file
        self.config_dict = config_dict
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


class GPIOController(object):

    def _initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._gpio = GPIO
        if self.event_handlers:
            self.event_handlers = self.event_handlers(self._gpio)
