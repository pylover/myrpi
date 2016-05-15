#! /usr/bin/env python3
# tail -n +1 -f b | ./carc.py
import RPi.GPIO as GPIO
import time
import sys
import traceback
import select

io1_pin = 21  # rpi: 40   gray
io2_pin = 26  # rpi: 37   violet
io3_pin = 20  # rpi: 38   blue
io4_pin = 19  # rpi: 35   green
led_pin = 13  # rpi: 33   yellow
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(io1_pin, GPIO.OUT)
GPIO.setup(io2_pin, GPIO.OUT)
GPIO.setup(io3_pin, GPIO.OUT)
GPIO.setup(io4_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)

GPIO.output(led_pin, GPIO.LOW)


def reset_io_pins():
    GPIO.output(io1_pin, GPIO.LOW)
    GPIO.output(io2_pin, GPIO.LOW)
    GPIO.output(io3_pin, GPIO.LOW)
    GPIO.output(io4_pin, GPIO.LOW)


def sleep(func):
    def wrapper(c):
        command, delay = c
        GPIO.output(led_pin, GPIO.LOW)
        func(command)
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(delay)
        reset_io_pins()
        GPIO.output(led_pin, GPIO.LOW)
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


def quit(*a):
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
            'quit': quit,
            'exit': quit,
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
        quit()


if __name__ == '__main__':
    main()
