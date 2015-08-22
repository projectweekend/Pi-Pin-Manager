import unittest

from pi_pin_manager.pins import Pin
from pi_pin_manager.mocks import MockGPIO


PIN_CONFIG = {
    18: {
        'mode': 'OUT',
        'initial': 'LOW',
        'resistor': 'PUD_DOWN'
    },
    24: {
        'mode': 'IN',
        'initial': 'HIGH',
        'resistor': 'PUD_DOWN'
    }
}


class PinModelTestCase(unittest.TestCase):

    def setUp(self):
        super(PinModelTestCase, self).setUp()
        self.gpio = MockGPIO()

    def test_create_pin_with_valid_data(self):
        pin = Pin(
            number=18,
            mode='OUT',
            initial='LOW',
            resistor='PUD_OFF',
            gpio=self.gpio)

        self.assertEqual(pin.number, 18)
        self.assertEqual(pin.mode, 'OUT')
        self.assertEqual(pin.initial, 'LOW')
        self.assertEqual(pin.resistor, 'PUD_OFF')
        self.assertEqual(pin._gpio, self.gpio)

        settings = pin.settings
        self.assertEqual(settings['number'], 18)
        self.assertEqual(settings['mode'], 'OUT')
        self.assertEqual(settings['initial'], 'LOW')
        self.assertEqual(settings['resistor'], 'PUD_OFF')

    def test_create_pin_with_invalid_pin(self):
        self.assertRaises(ValueError, Pin, 'not int', 'OUT', 'LOW', 'PUD_OFF', self.gpio)

    def test_create_pin_with_invalid_mode(self):
        self.assertRaises(ValueError, Pin, 18, 'not', 'LOW', 'PUD_OFF', self.gpio)

    def test_create_pin_with_invalid_initial(self):
        self.assertRaises(ValueError, Pin, 18, 'OUT', 'not', 'PUD_OFF', self.gpio)

    def test_create_pin_with_invalid_resistor(self):
        self.assertRaises(ValueError, Pin, 18, 'OUT', 'LOW', 'not', self.gpio)

    def test_read_pin(self):
        pin = Pin(
            number=18,
            mode='OUT',
            initial='LOW',
            resistor='PUD_OFF',
            gpio=self.gpio)
        reading = pin.read()
        self.assertEqual(reading, 0)

    def test_turn_pin_on(self):
        pin = Pin(
            number=18,
            mode='OUT',
            initial='LOW',
            resistor='PUD_OFF',
            gpio=self.gpio)
        pin.on()
        reading = pin.read()
        self.assertEqual(reading, 1)

    def test_turn_pin_off(self):
        pin = Pin(
            number=18,
            mode='OUT',
            initial='LOW',
            resistor='PUD_OFF',
            gpio=self.gpio)

        pin.on()
        reading = pin.read()
        self.assertEqual(reading, 1)

        pin.off()
        reading = pin.read()
        self.assertEqual(reading, 0)

    def test_generate_pins_from_config(self):
        pins = Pin.generate_pins(PIN_CONFIG, self.gpio)
        for pin in pins:
            self.assertTrue(isinstance(pin, Pin))
