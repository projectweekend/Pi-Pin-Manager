from time import sleep
from gpio_config import GPIOConfig
from gpio_actions import GPIOActions
from errors import PinConfigurationError


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
        self._setup_pin(self._pin_config[0])

    def _validate_pin_config(self):
        if len(self._pin_config) != 1:
            message = 'Only one pin can be defined for a SinglePinWatcher'
            raise PinConfigurationError(message)
        required_keys = ['mode', 'event']
        if not set(required_keys) < set(self._pin_config[0].keys()):
            message = 'Pin config requires properties: {0}'.format(', '.join(required_keys))
            raise PinConfigurationError(message)

    def start(self):
        config = self._pin_config[0]
        pin = config['pin']
        event = getattr(self._gpio, config['event'])
        bounce = config.get('bounce', 0)
        try:
            while True:
                self._gpio.wait_for_edge(pin, event)
                self._action(self._gpio)
                sleep(bounce/1000.0)
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
