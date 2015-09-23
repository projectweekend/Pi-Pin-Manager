from distutils.core import setup

setup(
    name='Pi-Pin-Manager',
    version='3.1.0',
    author='Brian Hines',
    author_email='brian@projectweekend.net',
    packages=['pi_pin_manager'],
    url='http://projectweekend.github.io/Pi-Pin-Manager/',
    license='LICENSE.txt',
    description='Setup Raspberry Pi GPIO pins using a configuration file, not boilerplate.',
    long_description=open('README.txt').read(),
    install_requires=[
        "PyYAML == 3.11",
        "RPi.GPIO == 0.5.11",
    ],
)
