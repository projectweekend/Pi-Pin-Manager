from cerberus import Validator


CONFIG_SCHEMA = {
    'pin': {
        'type': 'integer',
        'required': True
    },
    'mode': {
        'type': 'string',
        'required': True,
        'is_pin_mode': True
    },
    'initial': {
        'type': 'string',
        'required': False,
        'is_initial': True
    },
    'resistor': {
        'type': 'string',
        'required': False,
        'is_resistor': True
    },
    'event': {
        'type': 'string',
        'required': False,
        'is_event': True
    },
    'handler': {
        'type': 'string',
        'required': False
    },
    'bounce': {
        'type': 'integer',
        'required': False,
    }
}


class ConfigValidator(Validator):

    def _validate_is_pin_mode(self, is_pin_mode, field, value):
        modes = ('IN', 'OUT', )
        if is_pin_mode and not value in modes:
            message = "Must be one of: {0}".format(', '.join(modes))
            self._error(field, message)

    def _validate_is_initial(self, is_initial, field, value):
        initial_values = ('LOW', 'HIGH', )
        if is_initial and not value in initial_values:
            message = "Must be one of: {0}".format(', '.join(initial_values))
            self._error(field, message)

    def _validate_is_resistor(self, is_resistor, field, value):
        resistor_values = ('PUD_UP', 'PUD_DOWN', )
        if is_resistor and not value in resistor_values:
            message = "Must be one of: {0}".format(', '.join(resistor_values))
            self._error(field, message)

    def _validate_is_event(self, is_event, field, value):
        event_values = ('RISING', 'FALLING', 'BOTH', )
        if is_event and not value in event_values:
            message = "Must be one of: {0}".format(', '.join(event_values))
            self._error(field, message)
