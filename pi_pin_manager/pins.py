import yaml
import RPi.GPIO as GPIO


class PinNotDefinedError(Exception):
	pass


class PinConfigurationError(Exception):
	pass


class PinManager(object):

	def __init__(self, config_file):
		self.config_file = config_file
		# self.handler_file = handler_file
		self._load_config()
		self._initialize_gpio()
		self._initialize_pins()

	def _initialize_gpio(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		self._gpio = GPIO

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

	def get_config(self, pin_number):
		try:
			return self.pin_config[pin_number].copy()
		except KeyError:
			message = "Pin {0} not defined in '{1}'".format(pin_number, self.config_file)
			raise PinNotDefinedError(message)

	def read(self, pin_number):
		self.get_config(pin_number)
		return self._gpio.input(pin_number)

	def write(self, pin_number, value):
		config = self.get_config(pin_number)
		if config['mode'] != 'OUT':
			message = "Pin {0} not set as 'OUT' in '{1}'".format(pin_number, self.config_file)
			raise PinConfigurationError(message)
		self._gpio.output(pin_number, value)
