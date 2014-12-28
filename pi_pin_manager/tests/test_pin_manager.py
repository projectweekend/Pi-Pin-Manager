import unittest

from pi_pin_manager import PinManager, PinConfigurationError, PinNotDefinedError


class PinManagerTests(unittest.TestCase):

	def setUp(self):
		self.manager = PinManager(
						config_file="./testing/test.yml",
						handler_file="./testing/handlers.py")

	def test_get_config(self):
		# undefined pin
		self.assertRaises(PinNotDefinedError, self.manager.get_config, 21)

		# good pin
		result = self.manager.get_config(23)
		self.assertEqual(result['mode'], 'IN')
		self.assertEqual(result['resistor'], 'PUD_DOWN')
		self.assertEqual(result['event'], 'RISING')
		self.assertEqual(result['bounce'], 200)

	def test_read(self):
		# undefined pin
		self.assertRaises(PinNotDefinedError, self.manager.read, 21)

		# good pin
		result = self.manager.read(23)
		self.assertEqual(result, 0)

	def test_write(self):
		# undefined pin
		self.assertRaises(PinNotDefinedError, self.manager.write, 21, 1)

		# misconfigured pin
		self.assertRaises(PinConfigurationError, self.manager.write, 23, 1)

		# good pin
		result = self.manager.read(18)
		self.assertEqual(result, 0)

		self.manager.write(18, 1)

		result = self.manager.read(18)
		self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
