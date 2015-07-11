from pi_pin_manager import MultiplePinWatcher


class EventHandler(object):

    def __init__(self, gpio):
        self.gpio = gpio

    def do_something(self, pin):
        print("Button pressed!")

    def do_something_else(self, pin):
        print("Button pressed!")


def main():
    config = [
        {
            'pin': 23,
            'mode': 'IN',
            'resistor': 'PUD_UP',
            'event': 'BOTH',
            'bounce': 300,
            'handler': 'do_something'
        },
        {
            'pin': 18,
            'mode': 'IN',
            'resistor': 'PUD_UP',
            'event': 'BOTH',
            'bounce': 300,
            'handler': 'do_something_else'
        }
    ]
    watcher = MultiplePinWatcher(config=config, event_handler=EventHandler)
    watcher.start()


if __name__ == '__main__':
    main()
