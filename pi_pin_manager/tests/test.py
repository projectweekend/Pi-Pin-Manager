import time
from pi_pin_manager import PinManager


class EventHandlers(object):
	def do_something(self, pin_num):
		print("BAM!")


pins = PinManager(config_file='pins.yml', event_handlers=EventHandlers())


if __name__ == '__main__':

	pins.write(18, 1)
	print("Pin 18 is: {0}".format(pins.read(18)))
	time.sleep(2)
	pins.write(18, 0)

	pins.on(18)
	print("Pin 18 is: {0}".format(pins.read(18)))
	time.sleep(2)
	pins.off(18)

	print("Config for pin 23:")
	print(pins.get_config(23))

	print("Push the button to test event handler...")

	while True:
		pass
