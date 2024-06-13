import OPi.GPIO as GPIO
import time

STEP_PIN = 'PL8'
DIR_PIN = 'PH3'
ENABLE_PIN = 'PD21'

frequency = 1000  # Время между импульсами в мкс (минимум 100)


def delay_microseconds(seconds):
    time.sleep(seconds / 1000000)


def setup():
    GPIO.setmode(GPIO.SUNXI)
    GPIO.setwarnings(False)
    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(ENABLE_PIN, GPIO.OUT)

    GPIO.output(ENABLE_PIN, GPIO.HIGH)


if __name__ == '__main__':
    setup()

    while True:
        GPIO.output(ENABLE_PIN, GPIO.LOW)
        GPIO.output(DIR_PIN, GPIO.HIGH)
        timing = time.time()
        while time.time() - timing < 3:
            GPIO.output(STEP_PIN, GPIO.HIGH)
            delay_microseconds(frequency)
            GPIO.output(STEP_PIN, GPIO.LOW)
        GPIO.output(ENABLE_PIN, GPIO.HIGH)
        time.sleep(3)

        GPIO.output(ENABLE_PIN, GPIO.LOW)
        GPIO.output(DIR_PIN, GPIO.LOW)
        timing = time.time()
        while time.time() - timing < 3:
            GPIO.output(STEP_PIN, GPIO.HIGH)
            delay_microseconds(frequency)
            GPIO.output(STEP_PIN, GPIO.LOW)
        GPIO.output(ENABLE_PIN, GPIO.HIGH)
        time.sleep(3)
