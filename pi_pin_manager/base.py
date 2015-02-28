import yaml
import RPi.GPIO as GPIO

from exceptions import PinNotDefinedError


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
