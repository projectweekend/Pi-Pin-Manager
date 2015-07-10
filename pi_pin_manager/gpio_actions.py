import RPi.GPIO as GPIO


class GPIOActions(object):

    def _initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._gpio = GPIO
        if self._event_handler:
            self._event_handler = self._event_handler(self._gpio)

    def _setup_pin(self, options):
        number = options['pin']
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
