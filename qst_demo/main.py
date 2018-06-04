import RPi.GPIO as GPIO
import threading
import time
import sys
import os


class Looper(threading.Thread):
    def __init__(self, loop_func, pause=1):
        super(Looper, self).__init__()
        self.stop_event = threading.Event()
        self.loop_func = loop_func
        self.pause = pause

    def run(self):
        while not self.stop_event.is_set():
            self.loop_func()
            time.sleep(self.pause)

    def stop(self):
        self.stop_event.set()


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

red_led = 12
green_led = 16
led_left = 26
led_right = 19

GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(led_left, GPIO.OUT)
GPIO.setup(led_right, GPIO.OUT)


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


def backward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)


def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)


def blink():
    pause = 0.1

    GPIO.output(green_led, GPIO.HIGH)
    time.sleep(pause)
    GPIO.output(green_led, GPIO.LOW)

    GPIO.output(red_led, GPIO.HIGH)
    time.sleep(pause)
    GPIO.output(red_led, GPIO.LOW)


try:
    # Just to make sure that LEDs are turned off.
    GPIO.output(red_led, GPIO.LOW)
    GPIO.output(green_led, GPIO.LOW)

    GPIO.output(led_left, GPIO.HIGH)
    GPIO.output(led_right, GPIO.HIGH)
    time.sleep(1)

    GPIO.output(green_led, GPIO.HIGH)
    GPIO.output(red_led, GPIO.HIGH)
    time.sleep(1)

    blinking = Looper(blink, pause=0.0)
    blinking.start()
    steps = 13
    delay = 3.0
    pause = 0.5
    for i in range(4):
        backward(int(delay) / 1000.0, int(steps))
        time.sleep(pause)
        backward(int(delay) / 1000.0, 37)
        time.sleep(pause)

    blinking.stop()
    blinking.join()
    GPIO.output(green_led, GPIO.HIGH)
    GPIO.output(red_led, GPIO.HIGH)
    time.sleep(2)

    GPIO.output(led_left, GPIO.LOW)
    GPIO.output(led_right, GPIO.LOW)

    print("Stop")
    setStep(0, 0, 0, 0)  # To release the coils.
    GPIO.cleanup()

except KeyboardInterrupt:
    print("Finish...")
    setStep(0, 0, 0, 0)
    GPIO.cleanup()
