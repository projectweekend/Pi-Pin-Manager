Boilerplate code is annoying and sometimes there can be a lot of it working with [Raspberry Pi GPIO](https://pypi.python.org/pypi/RPi.GPIO). I got tired of setting the board mode and declaring GPIO channels in every script so I made a library that uses a config file instead. In addition to getting rid of the boilerplate, **Pi-Pin-Manager** has the added benefit of pulling the configuration out of the code. This means you can modify any pin's behavior without ever touching a Python file or having to redeploy your program.


### Install it

```
pip install Pi-Pin-Manager
```

### Configure it

When creating an instance of `pi_pin_manager.PinManager`, there are two ways you can supply pin configuration information: A config file, written in [YAML](http://en.wikipedia.org/wiki/YAML) or a dictionary. If a pin is not defined at this step it will not be available to the `PinManager`.

#### With file

The following snippet shows an example configuration file:

```yaml
18:
  mode: OUT
  initial: HIGH
23:
  mode: OUT
  initial: LOW
24:
  mode: IN
  event: RISING
  handler: do_something
  bounce: 200
```

#### With dictionary

This snippet shows the same configuration example above as a dictionary:

```python
config = {
  18:
    'mode': 'OUT'
    'initial': 'HIGH'
  23:
    'mode': 'OUT'
    'initial': 'LOW'
  24:
    'mode': 'IN'
    'event': 'RISING'
    'handler': 'do_something'
    'bounce': 200
}
```

#### Notes

* Add a numbered element for each pin to enable
* `mode` - This controls whether the pin will be used for input or output. Accepted values are: `IN`, `OUT`. (Required)
* `initial` - This controls the starting value of the pin. Accepted values are: `LOW`, `HIGH`. (Optional - defaults to `LOW`)
* `resistor` - This controls the software defined pull up/pull down resistor available in the Broadcom SOC. Accepted values are: `PUD_UP`, `PUD_DOWN`. (Optional - defaults to none)
* `event` - This is used in combination with a pin set to input mode (`mode: IN`). Accepted values are: `RISING`, `FALLING`, `BOTH`.
* `handler` - This is used in combination with an `event` to designate a function to call when an `event` happens. This value should correspond to a method defined in your handler class.
* `bounce` - This can be used when an `event` is defined to prevent multiple `handler` calls being fired accidentally. The value is the number of milliseconds to wait before detecting another `event`.

For full documentation about available GPIO input pin configurations see the [documentation](http://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/).


### Single Pin Watcher

Sometimes, you just need something to watch for an event on one pin and fire off a custom function when that event is detected. This is a perfect use case for the `SinglePinWatcher`. It takes two parameters:
* A config file or dictionary as outlined above. However this config can only have one pin defined. If more than one pin definition is found a `PinConfigurationError` will be raised.
* An action function. This function will be called each time the pin `event` (from config) is detected. The function you define for this must accept a single parameter. An instance of the GPIO module will be passed into the function when it is called. This allows you to check the value of the pin in situations where you are detecting both (`event: BOTH`) a rising and falling event.

**Example Config File:**
```yaml
23:
  mode: IN
  initial: HIGH
  resistor: PUD_UP
  event: BOTH
  bounce: 200
```


```python
from pi_pin_manager import SinglePinWatcher

def my_action(gpio):
  # Whatever you want to happen when an event is detected goes here
  print("Event detected!")
  print(gpio.input(23))

watcher = SinglePinWatcher(config='path/to/config/file.yml', action=my_action)

watcher.start()
```


### Multiple Pin Watcher

The `MultiplePinWatcher` can simultaneously watch multiple pins, and fire off custom actions when events are detected. It takes two parameters:
* A config file or dictionary as outlined above.
* An event handler class. The class contstructor must take one parameter. An instance of the GPIO module will be passed into the constructor when it is called. This class must also have method names that match the `handler` names used in the config file. The methods you define for this must accept a single parameter. The number of the pin will be passed in automatically into the method when it is called.

**Example Config File:**
```yaml
18:
  mode: IN
  initial: HIGH
  resistor: PUD_UP
  event: FALLING
  bounce: 200
  handler: do_something

23:
  mode: IN
  initial: HIGH
  resistor: PUD_UP
  event: BOTH
  bounce: 200
  handler: do_something_else
```


```python
from pi_pin_manager import MultiplePinWatcher


class MyHandler(object):

  def __init__(self, gpio):
    self._gpio = gpio

  def do_something(self, pin):
    # Whatever you want to happen when an event is detected goes here
    print("PIN {0}!!!".format(pin))

  def do_something_else(self, pin):
    # Whatever you want to happen when an event is detected goes here
    print("PIN {0}!!!".format(pin))

watcher = MultiplePinWatcher(config='path/to/config/file.yml', event_handler=MyHandler)

watcher.start()
```


### Pin Manager (no event)

```python
from pi_pin_manager import PinManager


# With configuration file
pins = PinManager(config_file='path/to/config/file.yml')

# With configuration dictionary, assuming my_config_dictionary was defined
# pins = PinManager(config_dict=my_config_dictionary)


# Read a pin
result = pins.read(18)

# Write to a pin
pins.write(19, 1)

# Turn pin on
pins.on(19)

# Turn pin off
pins.off(19)

# Get configuration for a pin
result = pins.get_config(23)

# Get configuration for all pins
result = pins.get_config()

# Cleanup GPIO on single pin
pins.cleanup(18)

# Cleanup GPIO on all pins
pins.cleanup()
```

### Pin Manager (with event)

If an `event` and `handler` have been defined for a pin in the config file, then you must also provide a class that contains the callbacks to execute. Each method you add to this class should match the name of a `handler` value. Based on the example code below, `handler: do_something` is expected in the config file `path/to/config/file.yml`.

```python
from pi_pin_manager import PinManager


class EventHandlers(object):

    def __init__(self, gpio):
      self._gpio = gpio

    def do_something(self, pin_number):
        # Whatever you want to trigger when an event is detected goes here
        # You have access to the GPIO object as self._gpio
        print('pin {0}'.format(pin_number))


pins = PinManager(config_file='path/to/config/file.yml', event_handlers=EventHandlers)

# With configuration dictionary, assuming my_config_dictionary was defined
# pins = PinManager(config_dict=my_config_dictionary, event_handlers=EventHandlers)
```

### Exceptions

This package may raise the following custom exceptions:

* `PinNotDefinedError` - This is raised when attempting to `read` or `write` to a pin that is not defined in the configuration file.
* `PinConfigurationError` - This is raised when attempting to perform an action on a pin that does not match its configuration. For example, trying to `write` to a pin not defined as `mode: OUT`.
