import yaml
from time import sleep
import RPi.GPIO as GPIO

from base import GPIOConfig, GPIOActions
from exceptions import PinConfigurationError, PinNotDefinedError


class SinglePinWatcher(GPIOConfig, GPIOActions):
    """This class is used with a single pin only. Calling the 'start' method will
    block, waiting for the defined change in pin state. When that happens the
    function passed into the 'action' parameter is called. When you define this
    function, it can accept a single argument 'gpio'. An instance of GPIO will
    be passed in so you can check the state of a pin when firing actions on BOTH
    rising/falling edges."""

    def __init__(self, config, action=None):
        super(SinglePinWatcher, self).__init__(config=config)
        self._action = action
        self._validate_pin_config()
        self._initialize_gpio()
        self._initialize_pins()

    def _validate_pin_config(self):
        if len(self._pin_config.keys()) != 1:
            message = 'Only one pin can be defined for a SinglePinWatcher'
            raise PinConfigurationError(message)
        pin = self._pin_config.keys()[0]
        required_keys = ['mode', 'event']
        if not set(required_keys) < set(self._pin_config[pin].keys()):
            message = 'Pin config requires properties: {0}'.format(', '.join(required_keys))
            raise PinConfigurationError(message)

    def _initialize_pins(self):
        for pin_num, pin_options in self._pin_config.items():
            self._setup_pin(pin_num, pin_options)

    def start(self):
        pin = self._pin_config.keys()[0]
        event = self._gpio.__getattribute__(self._pin_config[pin]['event'])
        bounce = self._pin_config[pin].get('bounce', 0)
        try:
            while True:
                self._gpio.wait_for_edge(pin, event)
                self._action(self._gpio)
                sleep(bounce/1000.0)
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()


class MultiplePinWatcher(GPIOConfig, GPIOActions):
    """This class is used with multiple pins. Calling the 'start' method will
    block, waiting for changes in state for the defined pins. When that happens
    a method on the `event_handler` class, matching the 'handler' name from the
    pin config is called. Each of these 'handler' methods takes a single argument,
    the pin number, which is passed in automatically by the RPi.GPIO library.

    The 'event_handler' class should have one parameter in its constructor. An
    instance of GPIO will be passed in so you have access to it in each custom
    'handler' method."""

    def __init__(self, config, event_handler):
        super(MultiplePinWatcher, self).__init__(config=config, event_handler=event_handler)
        self._validate_pin_config()
        self._initialize_gpio()
        self._initialize_pins()

    def _validate_pin_config(self):
        required_keys = ['mode', 'event', 'handler']
        for _, v in self._pin_config.iteritems():
            if not set(required_keys) < set(v.keys()):
                message = 'Pin config requires properties: {0}'.format(', '.join(required_keys))
                raise PinConfigurationError(message)

    def _initialize_pins(self):
        for pin_num, pin_options in self._pin_config.items():
            self._setup_pin(pin_num, pin_options)

    def start(self):
        try:
            # keep this running for the threaded callbacks
            while True:
                sleep(0.250)
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()


class GPIOHelper(GPIOConfig, GPIOActions):
    """This is a helper class that will configure GPIO from a file or dictionary.
    After that you have direct access to the RPi.GPIO module using the 'gpio'
    property. The rest is up to you."""

    def __init__(self, config):
        super(GPIOHelper, self).__init__(config=config)
        self._initialize_gpio()
        self._initialize_pins()
        self.gpio = self._gpio

    def _initialize_pins(self):
        for pin_num, pin_options in self._pin_config.items():
            self._setup_pin(pin_num, pin_options)


class PinManager(object):

    def __init__(self, config_file=None, config_dict=None, event_handlers=None):
        self.config_file = config_file
        self.config_dict = config_dict
        self.event_handlers = event_handlers
        self._load_pin_config()
        self._initialize_gpio()
        self._initialize_pins()

    def _initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._gpio = GPIO
        if self.event_handlers:
            self.event_handlers = self.event_handlers(self._gpio)

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

    def _initialize_pins(self):
        for pin_num, pin_options in self.pin_config.items():
            self._setup_pin(pin_num, pin_options)

    def get_config(self, pin_number=None):
        if pin_number:
            try:
                return self.pin_config[pin_number].copy()
            except KeyError:
                message = "Pin {0} not defined in configuration".format(pin_number)
                raise PinNotDefinedError(message)
        return self.pin_config.copy()

    def read(self, pin_number):
        self.get_config(pin_number)
        return self._gpio.input(pin_number)

    def write(self, pin_number, value):
        config = self.get_config(pin_number)
        if config['mode'] != 'OUT':
            message = "Pin {0} not set as 'OUT' in configuration".format(pin_number)
            raise PinConfigurationError(message)
        self._gpio.output(pin_number, value)

    def on(self, pin_number):
        self.write(pin_number, 1)

    def off(self, pin_number):
        self.write(pin_number, 0)

    def cleanup(self, pin_number=None):
        if pin_number:
            return self._gpio.cleanup(pin_number)
        return self._gpio.cleanup()
