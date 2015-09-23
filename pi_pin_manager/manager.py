import yaml

from pi_pin_manager.settings import LOW, NO_RESISTOR
from pi_pin_manager.pins import Pin


class PinManager(object):

    def __init__(self, config_file, gpio):
        self._gpio = gpio
        self._gpio.setmode(self._gpio.BCM)
        self._gpio.setwarnings(False)
        config = self._config_from_file(config_file=config_file)
        for pin in Pin.generate_pins(config=config, gpio=self._gpio):
            attribute_name = 'pin_{0}'.format(pin.number)
            setattr(self, attribute_name, pin)

    @staticmethod
    def _config_from_file(config_file):
        with open(config_file, 'rb') as f:
            config = yaml.load(f)
        for k, v in config.items():
            keys = v.keys()
            if 'mode' not in keys:
                message = "'mode' key is missing for pin {0} in config"
                raise ValueError(message.format(k))
            if 'initial' not in keys:
                config[k]['initial'] = LOW
            if 'resistor' not in keys:
                config[k]['resistor'] = NO_RESISTOR
        return config
