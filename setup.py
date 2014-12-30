from distutils.core import setup

setup(
    name='Pi-Pin-Manager',
    version='0.0.8',
    author='Brian Hines',
    author_email='brian@projectweekend.net',
    packages=['pi_pin_manager'],
    url='http://pypi.python.org/pypi/Pi-Pin-Manager/',
    license='LICENSE.txt',
    description='Setup Raspberry Pi GPIO pins using a configuration file, not boilerplate.',
    long_description=open('README.txt').read(),
    install_requires=[
        "PyYAML == 3.11",
        "RPi.GPIO == 0.5.8",
    ],
)
