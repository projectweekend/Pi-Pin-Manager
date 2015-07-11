from pi_pin_manager import SinglePinWatcher


def action(gpio):
    print("Button pressed!")


def main():
    config = {
        'pin': 23,
        'mode': 'IN',
        'resistor': 'PUD_UP',
        'event': 'BOTH',
        'bounce': 300
    }
    watcher = SinglePinWatcher(config=config, action=action)
    watcher.start()


if __name__ == '__main__':
    main()
