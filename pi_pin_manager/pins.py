from pi_pin_manager.settings import (
    PIN_MODES,
    PIN_INITIALS,
    PIN_RESISTORS,
    PIN_RISING_EVENT,
    PIN_FALLING_EVENT,
    PIN_BOTH_EVENT,
    PIN_EVENT_TYPES)


class Pin(object):

    def __init__(self, number, mode, initial, resistor, gpio):
        self.number = number
        self.mode = mode
        self.initial = initial
        self.resistor = resistor

        self._gpio = gpio
        self._setup_gpio_channel()

    def _setup_gpio_channel(self):
        mode = getattr(self._gpio, self.mode)
        initial = getattr(self._gpio, self.initial)
        resistor = getattr(self._gpio, self.resistor)
        self._gpio.setup(self.number, mode, initial=initial, pull_up_down=resistor)

    @classmethod
    def generate_pins(cls, config, gpio):
        for k, v in config.iteritems():
            yield cls(
                number=k,
                mode=v['mode'],
                initial=v['initial'],
                resistor=v['resistor'],
                gpio=gpio)

    @property
    def number(self):
        return self._pin_number

    @number.setter
    def number(self, number):
        if hasattr(self, '_pin_number'):
            raise AttributeError("'number' cannot be modified after Pin object is created")
        self._pin_number = int(number)

    @property
    def mode(self):
        return self._pin_mode

    @mode.setter
    def mode(self, mode):
        if hasattr(self, '_pin_mode'):
            raise AttributeError("'mode' cannot be modified after Pin object is created")
        if mode not in PIN_MODES:
            raise ValueError("'mode' must be one of: {0}".format(', '.join(PIN_MODES)))
        self._pin_mode = mode

    @property
    def initial(self):
        return self._pin_initial

    @initial.setter
    def initial(self, initial):
        if hasattr(self, '_pin_initial'):
            raise AttributeError("'initial' cannot be modified after Pin object is created")
        if initial not in PIN_INITIALS:
            raise ValueError("'initial' must be one of: {0}".format(', '.join(PIN_INITIALS)))
        self._pin_initial = initial

    @property
    def resistor(self):
        return self._pin_resistor

    @resistor.setter
    def resistor(self, resistor):
        if hasattr(self, '_pin_resistor'):
            raise AttributeError("'resistor' cannot be modified after Pin object is created")
        if resistor is not None and resistor not in PIN_RESISTORS:
            raise ValueError("'resistor' must be one of: {0}".format(', '.join(PIN_RESISTORS)))
        self._pin_resistor = resistor

    @property
    def settings(self):
        prefix = '_pin_'
        return {k.replace(prefix, ''): v
                for k, v in self.__dict__.items() if k.startswith(prefix)}

    def read(self):
        return self._gpio.input(self.number)

    def on(self):
        self._gpio.output(self.number, 1)

    def off(self):
        self._gpio.output(self.number, 0)

    def attach_action(self, event_type, action, bounce=200):
        if event_type == PIN_RISING_EVENT:
            gpio_event = self._gpio.RISING
        elif event_type == PIN_FALLING_EVENT:
            gpio_event = self._gpio.FALLING
        elif event_type == PIN_BOTH_EVENT:
            gpio_event = self._gpio.BOTH
        else:
            message = "'event_type' must be one of: {0}".format(', '.join(PIN_EVENT_TYPES))
            raise ValueError(message)
        self._gpio.add_event_detect(
            self.number,
            gpio_event,
            callback=action,
            bouncetime=bounce)
