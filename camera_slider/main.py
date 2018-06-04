import argparse
import platform
import time
import sys
import os

is_rasp = (platform.system() == "Linux")

if is_rasp:
    import RPi.GPIO as GPIO
else:
    print("This device probably doens't have RPi.GPIO package :(")
    exit()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

enable_pin = 18
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24
relay_pin = 9

GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

GPIO.output(enable_pin, 1)


def shoot(delay):
    GPIO.output(relay_pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(relay_pin, GPIO.HIGH)


def forward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)


def backwards(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        t2 = time.time()


def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)


####################################
# Max Steps: 28000
# Time per 1000: 12 sec with delay=3
####################################

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("direct", help="direction of the motor", type=int)
    parser.add_argument("limit", help="quantity of big steps", type=int)
    parser.add_argument("-d", "--delay", help="delay in forward/backwards",
                        default=3, type=float)
    parser.add_argument("-l", "--limit", help="quantity of big steps",
                        default=28, type=int)
    parser.add_argument("-p", "--pause", help="pause between big steps",
                        default=0, type=float)
    parser.add_argument("-s", "--steps", help="quantity of steps per big step",
                        default=1000, type=int)
    args = parser.parse_args()

    # WARNING: Something here is missed. Unfourtunately I forgot the idea
    # behind some of the variables.
    # FIXME: !!!
    direct = args.direct
    limit = args.limit
    pause = args.pause
    delay = args.delay
    steps = args.steps
    seconds = args.seconds
    number = args.number

    limit = number
    steps = int(28000. / float(limit))
    timing = (steps * limit * 4. * delay) / 1000.
    pause = int(((number * seconds) - timing) / limit)

    tot_time = int(timing + (pause * limit))
    # tot_time = int(((steps * limit * 4. * delay) / 1000.) + (pause * limit))

    print("|+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("|")
    print("+       Start with parameters:")
    print("| Direction: {}".format(direct))
    print("+ Big steps: {}".format(limit))
    print("| Steps per Big step: {}".format(steps))
    print("|        Total steps: {}".format(steps * limit))
    print("+ Pause: {} sec".format(pause))
    print("| Delay: {} msec".format(delay))
    print("+ Time per forward/backwards: {} sec".format((steps * 4. * delay) /
                                                        1000.))
    print("|        Total Time: {}h. {}m. {}s.".format(tot_time / 3600,
                                                       (tot_time / 60) % 3600,
                                                       tot_time % 60))
    print("|            ({} sec)".format(tot_time))
    print("|+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")

    count = 0

    while count < limit:
        count += 1
        shoot(seconds)

        t1 = time.time()
        if direct:
            forward(int(delay) / 1000.0, int(steps))
        else:
            backwards(int(delay) / 1000.0, int(steps))
        print("Curr.count: {}/{}".format(count, limit))
        t2 = time.time()
        print("It took: {}".format(t2 - t1))
        if pause:
            time.sleep(pause)

    print("Count is", count)
    print("Stop")
    setStep(0, 0, 0, 0)  # To release the coils.
    GPIO.cleanup()

except KeyboardInterrupt:
    print("Finish...")
    setStep(0, 0, 0, 0)
    GPIO.cleanup()
