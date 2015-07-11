from time import sleep
from gpio_config import GPIOConfig
from gpio_actions import GPIOActions
from errors import PinConfigurationError


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
        for config in self._pin_config:
            if not set(required_keys) < set(config.keys()):
                message = 'Pin config requires properties: {0}'.format(', '.join(required_keys))
                raise PinConfigurationError(message)

    def _initialize_pins(self):
        for config in self._pin_config:
            self._setup_pin(config)

    def start(self):
        try:
            # keep this running for the threaded callbacks
            while True:
                sleep(0.250)
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
