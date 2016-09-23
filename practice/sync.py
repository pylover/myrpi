import sys

import lirc


s = lirc.init('myrpi', config_filename='/home/vahid/.config/lircrc')


if __name__ == '__main__':
    try:
        while True:
            c = lirc.nextcode()
            print(c)
    except KeyboardInterrupt:
        lirc.deinit()
        sys.exit(1)


