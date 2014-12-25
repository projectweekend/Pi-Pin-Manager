import unittest
import mock

from pins import PinManager
from testing.mock_gpio import MockGPIO



@mock.patch('RPi.GPIO', MockGPIO)
class PinManagerTests(unittest.TestCase):

	def test_pin_manager(self):
		manager = PinManager()


if __name__ == '__main__':
    unittest.main()
