This utility exposes a class that wraps the [RPi.GPIO]() library so you can define and initialize GPIO pins using a cofiguration file.


### Example Configuration File

A config file `config/pins.yml` is used to define the initial setup for pins that will be accessible to the API. If a pin is not defined here it will not be available to the pin manager. For full documentation about available GPIO input pin configurations see the [documentation](http://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/).

```yaml
18:
  mode: OUT
  initial: HIGH
23:
  mode: OUT
  initial: LOW
  resistor: PUD_DOWN
24:
  mode: IN
  event: RISING
  bounce: 200
```

* Add a numbered element for each pin to enabled
* `mode` - This controls whether the pin will be used for input or output. Accepted values are: `IN`, `OUT`. (Required)
* `initial` - This controls the starting value of the pin. Accepted values are: `LOW`, `HIGH`. (Optional - defaults to `LOW`)
* `resistor` - This controls the software defined pull up/pull down resistor available in the Broadcom SOC. Accepted values are: `PUD_UP`, `PUD_DOWN`. (Optional - defaults to none)
* `event` - Not implemented...yet. Accepted values are: `RISING`, `FALLING`, `BOTH`.
* `bounce` - Not implemented...yet. This can be used when an `event` is defined to prevent multiple callbacks being fired accidentally. The value is the number of milliseconds to wait before detecting another `event`.


### Example Usage

```python
from pins import PinManager


manager = PinManager('path/to/config/file.yml')


# Read a pin
result = manager.read(18)

# Write to a pin
result = manager.write(19, 1)

# Get configuration for a pin
result = manager.get_config(23)
```
