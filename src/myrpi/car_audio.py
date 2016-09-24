
"""
Controlling car audio with raspberry-pi:

http://www.htmanual.net/hyundai_tucson_lm_2010_year_owners_manual-516.html

The schematic

    Yellow VCC   RPI pin #33 VCC  o--3.3V--------------------------------------------o -
                                      1N4148                            Car Audio steering remote control socket
    Green  IO #4 RPI pin #35 IO#4 o---->|------<1.8M>------+       +-----------------o +
                                                           |       |
    Blue   IO #3 RPI pin #38 IO#3 o---->|------<--1M>------+       |
                                                           |       |
    Violet IO #2 RPI pin #37 IO#2 o---->|------<470K>------+       |
                                                           |      /
    Gray   IO #1 RPI pin #40 IO#1 o---->|------<220K>------+-----|   BC547
                                                                  \>--+
                                                                    e |
                                                                      |
                                                                      |
    White  GND   RPI pin #39 GND  o-------------<3.3K>----------------+

"""

import asyncio

# noinspection PyUnresolvedReferences, PyPackageRequirements
import RPi.GPIO as GPIO

from aiolirc import listen_for


SHORT_DELAY = .2
LONG_DELAY = .8


IO1 = 21  # rpi: 40   gray
IO2 = 26  # rpi: 37   violet
IO3 = 20  # rpi: 38   blue
IO4 = 19  # rpi: 35   green
VCC = 13  # rpi: 33   yellow


class RPIGPIOContext(asyncio.Lock):

    async def __aenter__(self):
        # Acquiring lock
        await super().__aenter__()

        # Broadcom pin-numbering scheme
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(IO1, GPIO.OUT)
        GPIO.setup(IO2, GPIO.OUT)
        GPIO.setup(IO3, GPIO.OUT)
        GPIO.setup(IO4, GPIO.OUT)
        GPIO.setup(VCC, GPIO.OUT)
        GPIO.output(VCC, GPIO.LOW)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cleanup all GPIOs to low
        reset_io_pins()

        # Cleanup all GPIOs
        GPIO.cleanup()

        # Releasing lock
        await super().__aexit__(exc_type, exc_val, exc_tb)


def reset_io_pins():
    GPIO.output(IO1, GPIO.LOW)
    GPIO.output(IO2, GPIO.LOW)
    GPIO.output(IO3, GPIO.LOW)
    GPIO.output(IO4, GPIO.LOW)


def sleep(delay):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            GPIO.output(VCC, GPIO.LOW)
            await func(*args, **kwargs)
            GPIO.output(VCC, GPIO.HIGH)
            await asyncio.sleep(delay)
            GPIO.output(VCC, GPIO.LOW)
            reset_io_pins()
        return wrapper
    return decorator


@listen_for('amp power', repeat=6)
@sleep(LONG_DELAY)
async def amp_power(loop):
    print('AMP Power')
    GPIO.output(IO2, GPIO.HIGH)


@listen_for('amp next')
@sleep(SHORT_DELAY)
async def amp_next(loop):
    print('AMP next')
    GPIO.output(IO1, GPIO.HIGH)
    GPIO.output(IO2, GPIO.HIGH)
    GPIO.output(IO3, GPIO.HIGH)
    GPIO.output(IO4, GPIO.HIGH)


@listen_for('amp previous')
@sleep(SHORT_DELAY)
async def amp_prev(loop):
    print('AMP Prev')
    GPIO.output(IO1, GPIO.HIGH)


@listen_for('amp source')
@sleep(SHORT_DELAY)
async def amp_source(loop):
    print('AMP source')
    GPIO.output(IO2, GPIO.HIGH)


@listen_for('amp mute')
@sleep(SHORT_DELAY)
async def amp_mute(loop):
    print('AMP mute')
    GPIO.output(IO3, GPIO.HIGH)
    GPIO.output(IO4, GPIO.HIGH)


@listen_for('amp volume up')
@sleep(SHORT_DELAY)
async def amp_volume_up(loop):
    print('AMP Volume up')
    GPIO.output(IO3, GPIO.HIGH)


@listen_for('amp volume down')
@sleep(SHORT_DELAY)
async def amp_volume_down(loop):
    print('AMP Volume down')
    GPIO.output(IO4, GPIO.HIGH)
