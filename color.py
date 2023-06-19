import RPi.GPIO as GPIO
import time
from collections import Counter

s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10
NUM_MEASUREMENTS = 8


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)
    print("\n")


def get_color():
    setup()
    colors = []
    for _ in range(NUM_MEASUREMENTS):
        GPIO.output(s2, GPIO.LOW)
        GPIO.output(s3, GPIO.LOW)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        red = NUM_CYCLES / duration
        print("red value - ",red)

        GPIO.output(s2, GPIO.LOW)
        GPIO.output(s3, GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        blue = NUM_CYCLES / duration
        print("blue value - ",blue)

        GPIO.output(s2, GPIO.HIGH)
        GPIO.output(s3, GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        green = NUM_CYCLES / duration
        print("green value - ",green)

        if 13000 <= red <= 19000 and 10000 <= blue <= 17500 and 9000 <= green <= 14000:
            colors.append("B")
        elif 20000 <= red <= 35000 and 20000 <= blue <= 35000 and 15000 <= green <= 35000:
            colors.append("W")
        else:
            colors.append("U")
        time.sleep(1)

    # Finding the most common color among measurements
    counter = Counter(colors)
    most_common_color = counter.most_common(1)[0][0]
    GPIO.cleanup()
    return most_common_color
    
