from gpio_config import GPIOConfig
from gpio_actions import GPIOActions
from errors import PinConfigurationError


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
        for config in self._pin_config:
            self._setup_pin(config)

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
