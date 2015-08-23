Boilerplate code is annoying and sometimes there can be a lot of it working with [Raspberry Pi GPIO](https://pypi.python.org/pypi/RPi.GPIO). I got tired of setting the board mode and declaring GPIO channels in every script so I made a library that uses a config file instead. In addition to getting rid of the boilerplate, **Pi-Pin-Manager** offers a cleaner interface for working with [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO).


### Install it

```
pip install Pi-Pin-Manager
```

#### Example Config File

The following snippet shows an example configuration file:

```yaml
18:
  mode: OUT
  initial: LOW
23:
  mode: OUT
  initial: HIGH
24:  
  mode: IN
  resistor: PUD_UP
```


#### Notes

* Add a numbered item for each pin
* `mode` - This controls whether the pin will be used for input or output. Accepted values are: `IN`, `OUT`. (Required)
* `initial` - This controls the starting value of the pin. Accepted values are: `LOW`, `HIGH`. (Optional - defaults to `LOW`)
* `resistor` - This controls the software defined pull up/pull down resistor available in the Broadcom SOC. Accepted values are: `PUD_UP`, `PUD_DOWN`, `PUD_OFF`. (Optional - defaults to `PUD_OFF`)

For full documentation about available GPIO input pin configurations see the [documentation](http://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/).


#### Example

The following snippet demonstrates a `PinManager` instance using the example config file referenced above. The `PinManager` instance will have named attributes for each pin number you defined in the config file.

```python
import RPi.GPIO as GPIO
from pi_pin_manager import PinManager


CONFIG_FILE = 'path/to/config/file.yml'

manager = PinManager(config_file=CONFIG_FILE, gpio=GPIO)

# Turn on pin 18
manager.pin_18.on()

# Turn off pin 18
manager.pin_18.off()

# Read pin 18
manager.pin_18.read()

# Settings dictionary for pin 18
manager.pin_18.settings
```


#### Run Tests

```
nosetests -v --with-coverage --cover-erase --cover-package=pi_pin_manager --cover-html
```
