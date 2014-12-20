import os
import yaml
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class PinManager(object):

	def __init__(self, config_file):
		self.config_file = config_file
		self._load_config()
		self._gpio = GPIO
		self._initialize_pins()

	def _load_config(self):
		with open(self.config_file) as file_data:
			self.pin_config = yaml.safe_load(file_data)

	def _setup_pin(self, number, mode, initial, resistor):
	    mode = self._gpio.__getattribute__(mode)
	    initial = self._gpio.__getattribute__(initial)
	    if resistor:
	        resistor = self._gpio.__getattribute__(resistor)
	        self._gpio.setup(number, mode, initial=initial, pull_up_down=resistor)
	    else:
	        self._gpio.setup(number, mode, initial=initial)

	def _initialize_pins(self):
		for pin_num, pin_options in self.pin_config.items():
			initial = pin_options.get('initial', 'LOW')
			resistor = pin_options.get('resistor', None)
			self._setup_pin(pin_num, pin_options['mode'], initial, resistor)
