==============
Pi-Pin-Manager
==============

Boilerplate code is annoying and sometimes there can be a lot of it working with Raspberry Pi
GPIO (RPi.GPIO). I got tired of setting the board mode and declaring GPIO channels in every
script so I made a library that uses a config file instead. In addition to getting rid of the
boilerplate, **Pi-Pin-Manager** has the added benefit of pulling the configuration out of the
code. This means you can modify any pin's behavior without ever touching a Python file or
having to redeploy your program.

For additional documentation: https://github.com/projectweekend/Pi-Pin-Manager
