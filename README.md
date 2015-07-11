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
- pin: 18
  mode: OUT
  initial: HIGH
- pin: 23
  initial: LOW
- pin: 24
  mode: IN
  event: RISING
  handler: do_something
  bounce: 200
```

#### With list

This snippet shows the same configuration example above as a list:

```python
config = [
  {
    'pin': 18,
    'mode': 'OUT'
    'initial': 'HIGH'
  },
  {
    'pin': 23,
    'mode': 'OUT'
    'initial': 'LOW'
  },
  {
    'pin': 24,
    'mode': 'IN'
    'event': 'RISING'
    'handler': 'do_something'
    'bounce': 200
  }
]
```

#### Notes

* `pin` - The pin number
* `mode` - This controls whether the pin will be used for input or output. Accepted values are: `IN`, `OUT`. (Required)
* `initial` - This controls the starting value of the pin. Accepted values are: `LOW`, `HIGH`. (Optional - defaults to `LOW`)
* `resistor` - This controls the software defined pull up/pull down resistor available in the Broadcom SOC. Accepted values are: `PUD_UP`, `PUD_DOWN`. (Optional - defaults to none)
* `event` - This is used in combination with a pin set to input mode (`mode: IN`). Accepted values are: `RISING`, `FALLING`, `BOTH`.
* `handler` - This is used in combination with an `event` to designate a function to call when an `event` happens. This value should correspond to a method defined in your handler class.
* `bounce` - This can be used when an `event` is defined to prevent multiple `handler` calls being fired accidentally. The value is the number of milliseconds to wait before detecting another `event`.

For full documentation about available GPIO input pin configurations see the [documentation](http://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/).


### Single Pin Watcher

Sometimes, you just need something to watch for an event on one pin and fire off a function when that event is detected. This is a perfect use case for the `SinglePinWatcher`. It takes two parameters:
* A config file or list as outlined above. However this config can only have one pin defined. If more than one pin definition is found a `PinConfigurationError` will be raised.
* An action function. This function will be called each time the pin `event` (from config) is detected. The function you define for this must accept a single parameter. An instance of the GPIO module will be passed into the function when it is called. This allows you to check the value of the pin in situations where you are detecting both (`event: BOTH`) a rising and falling event.

**Example Config File:**
```yaml
- pin: 23
  mode: IN
  initial: HIGH
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
