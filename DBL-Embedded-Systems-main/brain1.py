#!/usr/bin/env python3

import serial
import time
import RPi.GPIO as GPIO
import time
from collections import Counter

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10
NUM_MEASUREMENTS = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(s2, GPIO.OUT)
GPIO.setup(s3, GPIO.OUT)
GPIO_TRIGGER = 17
GPIO_ECHO = 27
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def get_color():
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

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

def get_motion():

    dist = distance()

    # check if distance is within the desired range
    if 2.5 <= dist <= 3.5:
        print("Distance is within the desired range!")
        return(True)
    else:
        print ("Measured Distance = %.1f cm" % dist)
        return(False)

if __name__ == '__main__':
	try: 	motion = False
			color_detected = ""
			received_data = False
			while motion == False:
				print("checking for motion")
				motion = get_motion()
			#when motion is detected
			ser.write(b"M")
			#wait until disk is under light sensor
			time.sleep(12.5)
			color_detected = get_color()
			ser.write(color_detected.encode())
			#wait for instructions from the arduino
			while received_data == False:
				if ser.in_waiting > 0:
					data = ser.readline().decode().rstrip()
					print(data)
					received_data = True

			if data == "check if track is clear":
				while motion == True:
					motion = get_motion()
				#Tell the arduino that track is clear ->  Go extend fetching mechanism
				ser.write(b"G")

	except KeyboardInterrupt:
				print("Measurement stopped by User")
