import sys

import lirc


s = lirc.init('CAR_AMP', config_filename='../src/myrpi/conf/lircrc')


if __name__ == '__main__':
    try:
        while True:
            c = lirc.nextcode()
            print(c)
    except KeyboardInterrupt:
        lirc.deinit()
        sys.exit(1)


