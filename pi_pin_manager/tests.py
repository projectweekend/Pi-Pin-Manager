import unittest

from pi_pin_manager.pins import Pin
from pi_pin_manager.mocks import MockGPIO
from pi_pin_manager.manager import PinManager


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


class PinTestCase(unittest.TestCase):

    def setUp(self):
        super(PinTestCase, self).setUp()
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

    def test_changing_pin_attributes_after_creation(self):
        pin = Pin(
            number=18,
            mode='OUT',
            initial='LOW',
            resistor='PUD_OFF',
            gpio=self.gpio)

        self.assertRaises(AttributeError, setattr, pin, 'number', 23)
        self.assertRaises(AttributeError, setattr, pin, 'mode', 'IN')
        self.assertRaises(AttributeError, setattr, pin, 'initial', 'HIGH')
        self.assertRaises(AttributeError, setattr, pin, 'resistor', 'PUD_UP')

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

    def test_attach_action(self):
        pin = Pin(
            number=18,
            mode='OUT',
            initial='LOW',
            resistor='PUD_OFF',
            gpio=self.gpio)

        def my_action(channel):
            pass

        pin.attach_action(event_type='RISING', action=my_action)
        pin.attach_action(event_type='FALLING', action=my_action)
        pin.attach_action(event_type='BOTH', action=my_action)

        # Invalid event type
        self.assertRaises(ValueError, pin.attach_action, 'NOT_VALID', my_action)


class PinManagerTestCase(unittest.TestCase):

    def setUp(self):
        super(PinManagerTestCase, self).setUp()
        self.valid_config_file = './pi_pin_manager/test_valid_config.yml'
        self.invalid_config_file = './pi_pin_manager/test_invalid_config.yml'
        self.gpio = MockGPIO()

    def test_create_pin_manager_with_valid_config(self):
        manager = PinManager(config_file=self.valid_config_file, gpio=self.gpio)
        self.assertTrue(isinstance(manager.pin_18, Pin))
        self.assertTrue(isinstance(manager.pin_23, Pin))
        self.assertTrue(isinstance(manager.pin_24, Pin))

    def test_create_pin_manager_with_invalid_config(self):
        self.assertRaises(ValueError, PinManager, self.invalid_config_file, self.gpio)
