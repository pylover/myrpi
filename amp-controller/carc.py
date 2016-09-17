#! /usr/bin/env python3
"""
Controlling car audio with raspberry-pi

The schematic

    Yellow VCC   RPI pin #33 VCC o--3.3V--------------------------------------------o -
                                     1N4148                                              Car Audio steering remote control socket
    Green  IO #4 RPI pin #35 IO4 o---->|------<1.8M>------+       +-----------------o +
                                                          |       |
    Blue   IO #3 RPI pin #38 IO3 o---->|------<--1M>------+       |
                                                          |       |
    Violet IO #2 RPI pin #37 IO2 o---->|------<470K>------+       |
                                                          |      /
    Gray   IO #1 RPI pin #40 IO1 o---->|------<220K>------+-----|   BC547
                                                                 \>--+
                                                                   e |
                                                                     |
                                                                     |
    White  GND   RPI pin #39 GND o-------------<3.3K>----------------+



First of all you have to create a fifo:

    $ mkfifo cmd-channel.fifo

And then run this script to listen on stdin:

    $ tail -n +1 -f cmd-channel.fifo | ./carc.py

Or:

    $ ./carc.py < cmd-channel.fifo
    
After all, you may send the command using the fifo channel:

    $ echo "source:1" > cmd-channel.fifo


Hope you enjoy !
vahid.mardani@gmail.com


Changelog:

-

"""
# noinspection PyUnresolvedReferences, PyPackageRequirements
import RPi.GPIO as GPIO
import time
import sys
import traceback
import select

__version__ = '0.1.0'

io1_pin = 21  # rpi: 40   gray
io2_pin = 26  # rpi: 37   violet
io3_pin = 20  # rpi: 38   blue
io4_pin = 19  # rpi: 35   green
vcc_pin = 13  # rpi: 33   yellow
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(io1_pin, GPIO.OUT)
GPIO.setup(io2_pin, GPIO.OUT)
GPIO.setup(io3_pin, GPIO.OUT)
GPIO.setup(io4_pin, GPIO.OUT)
GPIO.setup(vcc_pin, GPIO.OUT)

GPIO.output(vcc_pin, GPIO.LOW)


def reset_io_pins():
    GPIO.output(io1_pin, GPIO.LOW)
    GPIO.output(io2_pin, GPIO.LOW)
    GPIO.output(io3_pin, GPIO.LOW)
    GPIO.output(io4_pin, GPIO.LOW)


def sleep(func):
    def wrapper(c):
        command, delay = c
        GPIO.output(vcc_pin, GPIO.LOW)
        func(command)
        GPIO.output(vcc_pin, GPIO.HIGH)
        time.sleep(delay)
        reset_io_pins()
        GPIO.output(vcc_pin, GPIO.LOW)
    return wrapper


@sleep
def command_next(c):
    GPIO.output(io1_pin, GPIO.HIGH)
    GPIO.output(io2_pin, GPIO.HIGH)
    GPIO.output(io3_pin, GPIO.HIGH)
    GPIO.output(io4_pin, GPIO.HIGH)


@sleep
def command_prev(c):
    GPIO.output(io1_pin, GPIO.HIGH)


@sleep
def command_source(c):
    GPIO.output(io2_pin, GPIO.HIGH)


@sleep
def command_mute(c):
    GPIO.output(io3_pin, GPIO.HIGH)
    GPIO.output(io4_pin, GPIO.HIGH)


@sleep
def command_volup(c):
    GPIO.output(io3_pin, GPIO.HIGH)


@sleep
def command_voldown(c):
    GPIO.output(io4_pin, GPIO.HIGH)


def command_not_found(c):
    print('Command not found: %s' % (c if isinstance(c, str) else '%s:%d' % c))


def command_quit(*a):
    reset_io_pins()
    GPIO.cleanup() # cleanup all GPIO
    sys.exit(0)


def dispatch(c):
    c = c.strip().lower()
    if not c:
        return
    try:
        command, delay = c.split(':')
        {
            'next': command_next,
            'prev': command_prev,
            'source': command_source,
            'mute': command_mute,
            'volup': command_volup,
            'voldown': command_voldown,
            'quit': command_quit,
            'exit': command_quit,
        }.get(command, command_not_found)((command, float(delay)))
    except ValueError:
        command_not_found(c)


def main():
    f = sys.stdin
    try:
        while True:
            r = select.select([f], [], [])[0]
            dispatch(r[0].readline())

    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print('CTRL+C is pressed.')
    except:
        traceback.print_exc()
    finally:
        command_quit()


if __name__ == '__main__':
    main()
