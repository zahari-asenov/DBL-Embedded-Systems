import RPi.GPIO as GPIO
import time
from collections import Counter

s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10
NUM_MEASUREMENTS = 6


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)
    print("\n")


def detect_color():
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

        GPIO.output(s2, GPIO.LOW)
        GPIO.output(s3, GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        blue = NUM_CYCLES / duration

        GPIO.output(s2, GPIO.HIGH)
        GPIO.output(s3, GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        green = NUM_CYCLES / duration

        if 14000 <= red <= 18000 and 14000 <= blue <= 17500 and 12000 <= green <= 15000:
            colors.append("B")
        elif 12000 <= red <= 35000 and 16000 <= blue <= 35000 and 15001 <= green <= 35000:
            colors.append("W")
        elif 13000 <= red <= 20000 and 10000 <= blue <= 15500 and 9000 <= green <= 12000:
            colors.append("N")
        else:
            colors.append("U")
        time.sleep(1)

    # Finding the most common color among measurements
    counter = Counter(colors)
    most_common_color = counter.most_common(1)[0][0]
    return most_common_color


def endprogram():
    GPIO.cleanup()


if __name__ == '__main__':

    setup()

    try:
        most_common_color = detect_color()
        print(f"The most common color detected is: {most_common_color}")

    except KeyboardInterrupt:
        endprogram()
