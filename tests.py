import unittest

from pins import PinManager


class PinManagerTests(unittest.TestCase):

	def test_pin_manager(self):
		manager = PinManager(config_file="./testing/test.yml")


if __name__ == '__main__':
    unittest.main()
