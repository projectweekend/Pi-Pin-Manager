class MockGPIO(object):

	def __init__(self):
		self.BCM = 'BCM'
		self.IN = 'IN'
		self.OUT = 'OUT'
		self.LOW = 'LOW'
		self.HIGH = 'HIGH'
		self.PUD_UP = 'PUD_UP'
		self.PUD_DOWN = 'PUD_DOWN'
		self.pin_map = {}

	def setmode(self, mode):
		pass

	def setwarnings(self, input):
		pass

	def setup(self, number, mode, initial='LOW', pull_up_down=None):
		self.pin_map[number] = initial
		pass

	def input(self, pin_number):
		if self.pin_map[pin_number] == self.HIGH:
			return 1
		return 0

	def output(self, pin_number, value):
		if value:
			self.pin_map[pin_number] = self.HIGH
		else:
			self.pin_map[pin_number] = self.LOW
