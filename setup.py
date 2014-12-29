from distutils.core import setup

setup(
    name='Pi-Pin-Manager',
    version='0.0.4',
    author='Brian Hines',
    author_email='brian@projectweekend.net',
    packages=['pi_pin_manager'],
    url='http://pypi.python.org/pypi/Pi-Pin-Manager/',
    license='LICENSE.txt',
    description='Manage RPi.GPIO pin definition and initialization with a config file.',
    long_description=open('README.md').read(),
    install_requires=[
        "PyYAML == 3.11",
        "RPi.GPIO == 0.5.8",
    ],
)
