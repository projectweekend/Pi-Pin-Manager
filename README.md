Boilerplate code is annoying and sometimes there can be a lot of it working with [Raspberry Pi GPIO](https://pypi.python.org/pypi/RPi.GPIO). I got tired of setting the board mode and declaring GPIO channels in every script so I made a library that uses a config file instead. In addition to getting rid of the boilerplate, **Pi-Pin-Manager** has the added benefit of pulling the configuration out of the code. This means you can modify any pin's behavior without ever touching a Python file or having to redeploy your program.


### Install it

```
pip install Pi-Pin-Manager
```

### Configure it

When creating an instance of `pi_pin_manager.PinManager`, there are two ways you can supply pin configuration information: A config file, written in [YAML](http://en.wikipedia.org/wiki/YAML) or a list of dictionaries. If a pin is not defined at this step it will not be available to the `PinManager`.

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
  resistor: PUD_UP
```


#### Notes

* Add a numbered item for each pin
* `mode` - This controls whether the pin will be used for input or output. Accepted values are: `IN`, `OUT`. (Required)
* `initial` - This controls the starting value of the pin. Accepted values are: `LOW`, `HIGH`. (Optional - defaults to `LOW`)
* `resistor` - This controls the software defined pull up/pull down resistor available in the Broadcom SOC. Accepted values are: `PUD_UP`, `PUD_DOWN`, `PUD_OFF`. (Optional - defaults to `PUD_OFF`)

For full documentation about available GPIO input pin configurations see the [documentation](http://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/).

#### Run Tests

```
nosetests -v --with-coverage --cover-erase --cover-package=pi_pin_manager --cover-html
```
